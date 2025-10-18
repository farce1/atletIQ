#!/usr/bin/env python3
"""
Example usage of the Form Agent.

This script demonstrates how to use the FormAgent to conduct structured
interviews and extract data using the Claude API.
"""

import asyncio
import json
from uuid import uuid4

from app.agent.engines.form_agent import get_form_agent
from app.schemas.agent.form_schemas import FormAgentRequest


async def demonstrate_health_assessment():
    """Demonstrate a health assessment form completion."""
    print("=== Health Assessment Form Demo ===\n")

    # Get the form agent
    form_agent = get_form_agent()

    # Create a new session
    session_id = uuid4()
    session = form_agent.create_session("health_assessment", session_id)
    print(f"Created session: {session_id}")
    print(f"Form: {session.form_template_id}\n")

    # Simulate user responses
    responses = [
        "25",  # age
        "Male",  # gender
        "Intermediate",  # fitness level
        "3-4 times",  # exercise frequency
        "Weight loss, Muscle gain",  # primary goals
        "No",  # injuries
        "No",  # medical conditions
        "7",  # experience rating
    ]

    for i, response in enumerate(responses, 1):
        print(f"Question {i}: {form_agent.get_current_question(session_id).text}")
        print(f"User response: {response}")

        # Process the response
        request = FormAgentRequest(session_id=session_id, user_input=response)

        result = await form_agent.process_response(request)
        print(f"Agent response: {result.message}")

        if result.current_question:
            print(f"Next question: {result.current_question.text}")

        print(f"Progress: {result.progress.progress_percentage:.1f}%")
        print("-" * 50)

        if result.is_complete:
            print("\n=== Form Completed! ===")
            print("Extracted data:")
            print(json.dumps(result.extracted_data, indent=2))
            break


async def demonstrate_user_onboarding():
    """Demonstrate a user onboarding form completion."""
    print("\n\n=== User Onboarding Form Demo ===\n")

    # Get the form agent
    form_agent = get_form_agent()

    # Create a new session
    session_id = uuid4()
    session = form_agent.create_session("user_onboarding", session_id)
    print(f"Created session: {session_id}")
    print(f"Form: {session.form_template_id}\n")

    # Simulate user responses
    responses = [
        "John Doe",  # full name
        "john.doe@example.com",  # email
        "+1-555-123-4567",  # phone
        "English",  # preferred language
        "Email, Push notifications",  # notification preferences
        "Yes",  # terms accepted
    ]

    for i, response in enumerate(responses, 1):
        current_question = form_agent.get_current_question(session_id)
        if not current_question:
            break

        print(f"Question {i}: {current_question.text}")
        print(f"User response: {response}")

        # Process the response
        request = FormAgentRequest(session_id=session_id, user_input=response)

        result = await form_agent.process_response(request)
        print(f"Agent response: {result.message}")

        if result.current_question:
            print(f"Next question: {result.current_question.text}")

        print(f"Progress: {result.progress.progress_percentage:.1f}%")
        print("-" * 50)

        if result.is_complete:
            print("\n=== Form Completed! ===")
            print("Extracted data:")
            print(json.dumps(result.extracted_data, indent=2))
            break


async def demonstrate_error_handling():
    """Demonstrate error handling with invalid responses."""
    print("\n\n=== Error Handling Demo ===\n")

    # Get the form agent
    form_agent = get_form_agent()

    # Create a new session
    session_id = uuid4()
    session = form_agent.create_session("health_assessment", session_id)
    print(f"Created session: {session_id}\n")

    # Test invalid responses
    invalid_responses = [
        "not_a_number",  # invalid age
        "25",  # valid age
        "Invalid Gender",  # invalid gender choice
        "Male",  # valid gender
        "Maybe",  # invalid yes/no response
        "Yes",  # valid yes/no response
    ]

    for i, response in enumerate(invalid_responses, 1):
        current_question = form_agent.get_current_question(session_id)
        if not current_question:
            break

        print(f"Question {i}: {current_question.text}")
        print(f"User response: {response}")

        # Process the response
        request = FormAgentRequest(session_id=session_id, user_input=response)

        result = await form_agent.process_response(request)
        print(f"Agent response: {result.message}")

        if result.error:
            print(f"Error: {result.error}")

        if result.current_question:
            print(f"Next question: {result.current_question.text}")

        print(f"Progress: {result.progress.progress_percentage:.1f}%")
        print("-" * 50)


async def main():
    """Run all demonstrations."""
    print("Form Agent Demonstration")
    print("=" * 50)

    # Show available templates
    form_agent = get_form_agent()
    templates = form_agent.get_form_templates()
    print("Available form templates:")
    for template_id, template in templates.items():
        print(f"  - {template_id}: {template.name}")
    print()

    # Run demonstrations
    await demonstrate_health_assessment()
    await demonstrate_user_onboarding()
    await demonstrate_error_handling()

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
