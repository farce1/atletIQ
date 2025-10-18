# AthletIQ Landing Page

An ultra-minimalistic, fast landing page for AthletIQ - your AI-powered personal trainer that uses Garmin and Apple Watch data.

## Features

- **Video Background**: Immersive background video with particles effect
- **Minimalistic Design**: Clean, modern interface with smooth animations
- **Magic UI Components**: Beautiful animations using blur-fade, text-animate, and particles
- **Social Integration**: Dropdown with multiple messaging platforms (Telegram, WhatsApp, Messenger, Signal, iMessage)
- **Responsive**: Works perfectly on all devices
- **Performance Optimized**: Built with Next.js 15 and React 19

## Tech Stack

- Next.js 15
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui
- Magic UI
- Lucide Icons

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run the development server:
```bash
npm run dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## Customization

### Update Telegram Link
Edit `/components/landing-page.tsx` line 76 and replace `https://t.me/yourusername` with your actual Telegram username.

### Change Video Background
Replace the video URL in `/components/landing-page.tsx` line 24 with your own video URL or local video file.

### Modify Colors
The gradient colors can be adjusted in the component classes:
- Purple to Pink gradient: `from-purple-600 to-pink-600`
- Feature tags use various colors: purple, pink, and blue

## Deployment

Deploy to Vercel:

```bash
npm run build
```

Then connect your repository to Vercel for automatic deployments.

## License

MIT
