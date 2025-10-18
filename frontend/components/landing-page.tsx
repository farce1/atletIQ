"use client";

import { BlurFade } from "@/components/ui/blur-fade";
import { TextAnimate } from "@/components/ui/text-animate";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { FaFacebookMessenger, FaWhatsapp, FaTelegram, FaApple } from "react-icons/fa";
import { SiSignal } from "react-icons/si";
import Image from "next/image";

export default function LandingPage() {
  return (
    <div className="relative h-screen w-full overflow-hidden bg-black">
      {/* Video Background */}
      <video
        autoPlay
        loop
        muted
        playsInline
        className="absolute inset-0 h-full w-full object-cover opacity-50"
      >
        <source
          src="https://vm.runware.ai/video/ws/5/vi/ed893243-4c25-40d6-8324-d423c56dc27f.mp4"
          type="video/mp4"
        />
      </video>

      {/* Dark Overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/30 via-black/20 to-black/30" />

      {/* Navigation */}
      <nav className="relative z-20 flex items-center justify-between px-8 py-6">
        <BlurFade delay={0.1} duration={0.6}>
          <Image
            src="https://im.runware.ai/image/ws/2/ii/86325b7c-4e3c-4276-beb0-a9e25758d6fc.png"
            alt="AthletIQ Logo"
            width={200}
            height={100}
            className="h-auto w-32 object-contain drop-shadow-[0_2px_8px_rgba(0,0,0,0.8)]"
          />
        </BlurFade>

        <BlurFade delay={0.2} duration={0.6}>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                size="lg"
                className="rounded-full bg-gradient-to-r from-purple-600 to-pink-600 px-8 font-semibold text-white shadow-lg shadow-purple-500/50 transition-all hover:scale-105 hover:shadow-purple-500/70"
              >
                Get Started
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent
              align="end"
              className="w-56 rounded-2xl border border-gray-800 bg-black/90 p-2 backdrop-blur-xl"
            >
              <DropdownMenuItem className="cursor-pointer rounded-xl p-3 text-white transition-colors hover:bg-[#0084FF]/20 hover:text-white focus:bg-[#0084FF]/20 focus:text-white">
                <FaFacebookMessenger className="mr-3 h-5 w-5 text-[#0084FF]" />
                <span>Messenger</span>
              </DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer rounded-xl p-3 text-white transition-colors hover:bg-[#25D366]/20 hover:text-white focus:bg-[#25D366]/20 focus:text-white">
                <FaWhatsapp className="mr-3 h-5 w-5 text-[#25D366]" />
                <span>WhatsApp</span>
              </DropdownMenuItem>
              <DropdownMenuItem
                className="cursor-pointer rounded-xl p-3 text-white transition-colors hover:bg-[#0088CC]/20 hover:text-white focus:bg-[#0088CC]/20 focus:text-white"
                asChild
              >
                <a
                  href="https://t.me/yourusername"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <FaTelegram className="mr-3 h-5 w-5 text-[#0088CC]" />
                  <span>Telegram</span>
                </a>
              </DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer rounded-xl p-3 text-white transition-colors hover:bg-[#3A76F0]/20 hover:text-white focus:bg-[#3A76F0]/20 focus:text-white">
                <SiSignal className="mr-3 h-5 w-5 text-[#3A76F0]" />
                <span>Signal</span>
              </DropdownMenuItem>
              <DropdownMenuItem className="cursor-pointer rounded-xl p-3 text-white transition-colors hover:bg-[#007AFF]/20 hover:text-white focus:bg-[#007AFF]/20 focus:text-white">
                <FaApple className="mr-3 h-5 w-5 text-[#007AFF]" />
                <span>iMessage</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </BlurFade>
      </nav>

      {/* Hero Content */}
      <div className="relative z-10 flex h-full flex-col items-center justify-center px-4 text-center">
        <div className="rounded-3xl border border-white/10 bg-gradient-to-br from-black/30 via-black/10 to-black/30 p-6 backdrop-blur-sm">
          <BlurFade delay={0.3} duration={0.8}>
            <div className="mb-6 flex justify-center">
              <Image
                src="https://im.runware.ai/image/ws/2/ii/86325b7c-4e3c-4276-beb0-a9e25758d6fc.png"
                alt="AthletIQ Logo"
                width={300}
                height={200}
                className="h-auto w-32 object-contain"
              />
            </div>
          </BlurFade>

          <BlurFade delay={0.5} duration={0.8}>
            <p className="mb-4 max-w-3xl text-xl font-light tracking-wide text-white sm:text-2xl md:text-3xl">
              Your AI-Powered Personal Trainer
            </p>
          </BlurFade>

          <BlurFade delay={0.7} duration={0.8}>
            <p className="max-w-2xl text-base text-gray-200 sm:text-lg md:text-xl">
              Harness the power of your Garmin and Apple Watch data to create
              personalized training plans tailored just for you
            </p>
          </BlurFade>

          {/* Feature Tags */}
          <BlurFade delay={0.9} duration={0.8}>
            <div className="mt-12 flex flex-wrap items-center justify-center gap-4">
              <div className="rounded-full border border-purple-500/30 bg-purple-500/10 px-6 py-2 text-sm text-purple-200 backdrop-blur-sm">
                Garmin Integration
              </div>
              <div className="rounded-full border border-pink-500/30 bg-pink-500/10 px-6 py-2 text-sm text-pink-200 backdrop-blur-sm">
                Apple Watch
              </div>
              <div className="rounded-full border border-blue-500/30 bg-blue-500/10 px-6 py-2 text-sm text-blue-200 backdrop-blur-sm">
                AI-Driven Insights
              </div>
            </div>
          </BlurFade>
        </div>
      </div>
    </div>
  );
}
