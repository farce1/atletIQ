from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from app.agent.engines.core_agent import (
    get_claude_agent,
    get_extractor_claude_agent,
    get_training_fitness_index_claude_agent,
    ClaudeAgentError,
)
from app.api.deps import get_db
from app.core.config import get_settings
from app.api.exceptions.chat_exceptions import conversation_not_found_error
from app.crud.chat import create_chat_session
from app.crud.conversation import create_conversation, get_conversation_by_session_id
from app.crud.message import create_message
from app.models import ChatSession, Conversation
from app.schemas.agent.message_roles import MessageRole
from app.schemas.message_schemas import MessageCreate

from app.core.config import CONVO_MAPPING


from app.agent.prompts.agent_prompts import TEXT_QUERY_PROMPT

# Global session state storage
SESSION_STATE = {}


class ChatService:
    def __init__(self, db: Session = Depends(get_db)):
        self._db = db
        self._settings = get_settings()

    def create_chat_session(self) -> UUID:
        try:
            chat_session = create_chat_session(session=self._db)
            session_id = chat_session.id
        except Exception:
            self._db.rollback()
            raise
        return session_id

    def get_or_create_session_for_string_id(self, string_id: str) -> UUID:
        """Get existing UUID for string_id or create new session and map it."""
        if string_id in CONVO_MAPPING.keys():
            print("Fetching existing session")
            return CONVO_MAPPING[string_id]
        print(CONVO_MAPPING)
        print(string_id)

        # Create new session and map the string_id to the UUID
        print("Creating new session")
        session_id = self.create_chat_session()
        CONVO_MAPPING[string_id] = session_id
        return session_id

    def get_session_uuid(self, string_id: str) -> Optional[UUID]:
        """Get UUID for string_id if it exists, otherwise return None."""
        return CONVO_MAPPING.get(string_id)

    def _get_session_state(self, session_id: str) -> dict:
        """Get session state for a given session ID."""
        if session_id not in SESSION_STATE:
            SESSION_STATE[session_id] = {
                "onboarding_completed": False,
                "profile_mapping": None,
                "wearable_tracking_completed": False,
                "profile_completion_completed": False,
            }
        return SESSION_STATE[session_id]

    def _set_onboarding_completed(self, session_id: str, completed: bool) -> None:
        """Set onboarding completion status for a session."""
        state = self._get_session_state(session_id)
        state["onboarding_completed"] = completed

    def _get_onboarding_completed(self, session_id: str) -> bool:
        """Get onboarding completion status for a session."""
        state = self._get_session_state(session_id)
        return state["onboarding_completed"]

    def _set_profile_mapping(self, session_id: str, profile: str) -> None:
        """Set profile mapping for a session."""
        state = self._get_session_state(session_id)
        state["profile_mapping"] = profile

    def _get_profile_mapping(self, session_id: str) -> Optional[str]:
        """Get profile mapping for a session."""
        state = self._get_session_state(session_id)
        return state["profile_mapping"]

    def _set_wearable_tracking_completed(
        self, session_id: str, completed: bool
    ) -> None:
        """Set wearable tracking completion status for a session."""
        state = self._get_session_state(session_id)
        state["wearable_tracking_completed"] = completed

    def _get_wearable_tracking_completed(self, session_id: str) -> bool:
        """Get wearable tracking completion status for a session."""
        state = self._get_session_state(session_id)
        return state.get("wearable_tracking_completed", False)

    def _set_profile_completion_completed(
        self, session_id: str, completed: bool
    ) -> None:
        """Set profile completion status for a session."""
        state = self._get_session_state(session_id)
        state["profile_completion_completed"] = completed

    def _get_profile_completion_completed(self, session_id: str) -> bool:
        """Get profile completion status for a session."""
        state = self._get_session_state(session_id)
        return state.get("profile_completion_completed", False)

    def get_chat_session_by_session_id(self, session_id: UUID) -> Optional[ChatSession]:
        statement = select(ChatSession).where(ChatSession.id == session_id)
        chat_session = self._db.execute(statement).scalars().first()
        return chat_session

    def delete_chat_session(self, db_obj: ChatSession):
        self._db.delete(db_obj)
        self._db.commit()

    def create_conversation(self, session_id: UUID | None) -> Conversation:
        try:
            conversation = create_conversation(session=self._db, session_id=session_id)
            return conversation
        except Exception:
            self._db.rollback()
            raise

    def add_message(
        self,
        session_external_id: str,
        content: str,
        role: MessageRole,
    ) -> None:
        session_id = CONVO_MAPPING.get(session_external_id)
        if session_id is None:
            raise conversation_not_found_error()

        try:
            conversation = get_conversation_by_session_id(
                session=self._db, session_id=session_id
            )

            if conversation is None:
                raise conversation_not_found_error()

            message = MessageCreate(
                conversation_id=conversation.id, role=role, content=content
            )
            create_message(session=self._db, message_in=message)
            self._db.commit()
        except Exception:
            self._db.rollback()
            raise

    async def process_query(
        self,
        message: str,
        chat_session_string_id: str,
    ) -> str:
        """Process a query using the Claude agent."""
        try:
            # Get or create session UUID for the string ID
            session_uuid = self.get_or_create_session_for_string_id(
                chat_session_string_id
            )

            # Ensure conversation exists for this session
            conversation = get_conversation_by_session_id(
                session=self._db, session_id=session_uuid
            )
            if conversation is None:
                conversation = self.create_conversation(session_uuid)

            # Get session state
            onboarding_completed = self._get_onboarding_completed(
                chat_session_string_id
            )
            profile_mapping = self._get_profile_mapping(chat_session_string_id)
            wearable_tracking_completed = self._get_wearable_tracking_completed(
                chat_session_string_id
            )
            profile_completion_completed = self._get_profile_completion_completed(
                chat_session_string_id
            )

            if not onboarding_completed:
                print("Onboarding")
                print(
                    f"Onboarding completed: {onboarding_completed}, Profile mapping: {profile_mapping}"
                )
                response_text = TEXT_QUERY_PROMPT
                self._set_onboarding_completed(chat_session_string_id, True)

            elif profile_mapping is None:
                print("Extracting profile")
                print(
                    f"Onboarding completed: {onboarding_completed}, Profile mapping: {profile_mapping}"
                )
                # Use extractor agent to extract user profile data from the message
                extractor_claude_agent = get_extractor_claude_agent()
                # Set the database session for loading chat history
                extractor_claude_agent.db_session = self._db

                # Process the message with the extractor agent
                extraction_response = await extractor_claude_agent.process_message(
                    session_id=session_uuid,
                    message=message,
                    stream=False,
                )

                try:
                    import logging

                    logger = logging.getLogger(__name__)

                    # Log the raw extraction response for debugging
                    logger.info(f"Raw extraction response: {extraction_response}")

                    # Store the formatted profile string directly
                    self._set_profile_mapping(
                        chat_session_string_id, extraction_response
                    )
                    response_text = (
                        "Thank you for providing your information! I've created your "
                        "profile with the details you shared."
                        "Do you use any devices to track your activity?"
                    )

                except Exception as e:
                    logger.error(f"Error during profile extraction: {e}")
                    logger.error(
                        f"Raw response that caused error: {extraction_response}"
                    )
                    # If extraction fails, store a default message and ask for more info
                    default_profile_text = (
                        "**Basic Information:**\n"
                        "- Age: Not specified\n"
                        "- Weight: Not specified\n"
                        "- Height: Not specified\n"
                        "- BMI: Not calculated\n\n"
                        "**Running Experience:**\n"
                        "- Started running: Not specified\n"
                        "- Years of experience: Not specified\n"
                        "- Personal Bests: None specified\n\n"
                        "**Health & Injuries:**\n"
                        "- Current injuries: None specified\n"
                        "- Injury history: Not mentioned\n\n"
                        "**Lifestyle:**\n"
                        "- Sleep: Not specified\n"
                        "- Job type: Not specified\n"
                        "- Gym access: Not specified\n"
                        "- Training time available: Not specified\n\n"
                        "**Goals:**\n"
                        "- Main running goal: Not specified\n"
                        "- Additional goals: None specified\n\n"
                        "**Fitness Level & Preferences:**\n"
                        "- Current fitness level: Not specified\n"
                        "- Preferred training times: Not specified\n"
                        "- Training preferences: Not specified"
                    )
                    self._set_profile_mapping(
                        chat_session_string_id, default_profile_text
                    )
                    response_text = "I had trouble extracting your information - we will skip that for now."
            elif not profile_completion_completed:
                print("Profile completion message")
                print(
                    f"Onboarding completed: {onboarding_completed}, "
                    f"Profile mapping: {profile_mapping}, "
                    f"Wearable tracking completed: {wearable_tracking_completed}, "
                    f"Profile completion completed: {profile_completion_completed}"
                )
                response_text = "Thank you, connecting to your data and I'm building your profile and calculating your performance, "
                claude_training_fitness_index_agent = (
                    get_training_fitness_index_claude_agent(
                        user_bio_profile=self._get_profile_mapping(
                            chat_session_string_id
                        )
                    )
                )
                # Set the database session for loading chat history
                claude_training_fitness_index_agent.db_session = self._db
                response_text += (
                    await claude_training_fitness_index_agent.process_message(
                        session_id=session_uuid,
                        message=profile_mapping,
                        stream=False,
                    )
                )

                self._set_profile_completion_completed(chat_session_string_id, True)
            else:
                print("Processing message")
                print(
                    f"Onboarding completed: {onboarding_completed}, "
                    f"Profile mapping: {profile_mapping}, "
                    f"Wearable tracking completed: {wearable_tracking_completed}, "
                    f"Profile completion completed: {profile_completion_completed}"
                )
                # Get Claude agent with user profile and process the message
                user_profile = self._get_profile_mapping(chat_session_string_id)
                claude_agent = get_claude_agent(user_bio_profile=user_profile)
                # Set the database session for loading chat history
                claude_agent.db_session = self._db
                response_text = await claude_agent.process_message(
                    session_id=session_uuid,
                    message=message,
                    stream=self._settings.CLAUDE_AGENT_ENABLE_STREAMING,
                )
            # Add user message to database
            self.add_message(chat_session_string_id, message, MessageRole.USER)
            # Add assistant response to database
            self.add_message(
                chat_session_string_id, response_text, role=MessageRole.ASSISTANT
            )

            return response_text

        except ClaudeAgentError as e:
            # Log the error and return a fallback response
            error_message = f"I apologize, but I encountered an error: {str(e)}"
            self.add_message(
                chat_session_string_id, error_message, role=MessageRole.ASSISTANT
            )
            return error_message
        except Exception:
            # Log unexpected errors and return a generic error message
            error_message = (
                "I apologize, but I encountered an unexpected error. Please try again."
            )
            self.add_message(
                chat_session_string_id, error_message, role=MessageRole.ASSISTANT
            )
            return error_message
