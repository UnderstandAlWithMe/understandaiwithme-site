---
title: How to Set Up a Salon Booking System With Automatic Reminders (No Coding)
description: Set up a simple salon booking system: clients book themselves, get a confirmation and two reminders, and buffer time keeps your day workable.
date: 2026-11-23
tile: build-ai-automation
video: 0OJn28OP4-M
video_live: 2026-11-26T19:00:00Z
---
Your phone buzzes mid-appointment. Someone wants to book, but you have scissors in your hand, and by the time you reply they may have gone elsewhere. Others book and then forget to turn up. A simple **salon booking system** fixes both problems: clients pick their own time on a booking page, get a confirmation straight away and get reminded before the appointment, while you keep working.

This guide shows hair salons, barbers, and nail and beauty studios how to set one up in an afternoon, without coding. AI helps with the wording so the page still sounds like you.

## What you will build

- A **booking page** where clients choose a service and a free time slot.
- An **instant confirmation email** with buttons the client can use to reschedule or cancel.
- **Two automatic reminder emails**, one the day before and one an hour before.
- **Buffer time and a daily limit**, so the page never books you back to back from opening to closing.

We use the Systeme.io booking calendar in our video. Systeme.io is an all-in-one tool for web pages, emails and bookings, and its booking calendar page says the calendar is included on the free plan. Plans change, so check its pricing page before you start. Our [Systeme.io review](/guides/systeme-io-review-for-tradespeople/) covers the free plan's limits, including what the email reminders can't do. If you want to follow along with the same tool, you can [open a free Systeme.io account](/go/systeme) (affiliate link: we may earn a commission at no extra cost to you). Any booking tool with reminders and buffer time works the same way.

## How to set up a salon booking system in five steps

### Step 1: Create a booking event for your most booked service

An "event" is simply one bookable service with a set length. In Systeme.io, open the **CRM** menu, choose **Calendar**, then the **Events** tab, and click **Create new event**. Choose **Individual event**, which means one client per time slot.

Name it after the service clients ask for most, such as "Cut and blow-dry, 45 minutes", and set the duration to match. For location, choose **In person** and add your salon address. Start with one service and add the others once it works.

### Step 2: Let AI write the booking page description

The description is the short text clients read before they book. Open ChatGPT, Claude or another AI assistant. If you already have a short "how we write" note (see our guide to [AI emails in your own voice](/guides/ai-email-templates-for-small-business/)), paste it in first. Then use this prompt and change the details:

"I run a small hair salon. Write a short, warm description for my online booking page for a 45-minute cut and blow-dry. Include where to park, that clients should arrive five minutes early, and that they can rebook or cancel up to 24 hours before. Under 80 words, friendly, no jargon."

Read the draft out loud and correct anything untrue: AI can invent details, such as a car park you do not have. This matters because in Systeme.io the reminder emails are written by the system and their wording cannot be edited, so your description is where your voice and your rules live.

### Step 3: Set your hours and check the reminders

Set your availability to the hours you actually want bookings, not every hour the salon is open. Leave room for walk-ins and lunch, and set a **minimum notice period** so nobody books a slot that starts in ten minutes.

Then look at the reminders. In Systeme.io, every new event comes with two by default: one 24 hours before and one an hour before. You can change the timings or add a third, up to three per event. For most salons the two defaults are a sensible start. Note that these reminders are emails, not text messages. If most of your clients only read texts, salon-specific booking software with SMS reminders may suit you better.

If you use Google Calendar, connect it in the event settings so new bookings appear there automatically, and block personal appointments in the booking calendar.

### Step 4: Add buffer time and a daily limit

This is the step most people skip. Open the event's advanced settings and add **buffer time**: ten or fifteen minutes after each appointment to sweep up, take payment and breathe before the next client sits down. Then set a **daily limit**, the most bookings of this service you want in one day.

Without these, a booking page will happily fill every minute of your day. While you are there, set a **cancellation deadline** that matches the rule you wrote in your description, such as 24 hours.

### Step 5: Share the page and test it

Put the booking calendar on a page, then add the link to your Instagram bio, your Google Business Profile, your website and your reply to every "do you have any space?" message.

Before you share it, book a slot yourself with a personal email address. Check the confirmation reads well on a phone and that the reschedule and cancel buttons work. Let one test booking run until the reminders arrive, then cancel it.

## Make online booking feel personal

Some owners worry that clients prefer to message because it feels more personal. A few small touches help.

- **Keep messaging for the tricky ones.** Colour corrections, bridal hair and first-time patch tests may still need a chat first. Say so on the page.
- **Be clear about your rules.** If you take deposits or charge for late cancellations, say so before people book. Payment links are a simple way to take one: see [card reader or payment links](/guides/card-reader-or-payment-links/).
- **Follow up after the visit.** A thank-you with a "book your next appointment" link works well, using the same idea as our [quote follow-up system](/guides/quote-follow-up-system-for-tradespeople/).

Deposit and cancellation-fee rules depend on consumer law where you work, so check your local guidance (for example the FTC in the US, GOV.UK in the UK or the ACCC in Australia) before you charge one.

If you want to see how many hours booking messages and other admin cost you each week, try the free [admin time calculator](https://understandaiwithme.com/tools/admin-time-calculator/). If you would rather have a booking system connected to your till, CRM or text messages built for you, see [get an AI automation built](/fix/build-ai-automation/).

## FAQ

### Do small salons need a booking system?

Not always. If you take a few bookings a week, messages may be enough. A booking system pays off when you miss enquiries while you are with a client, or spend evenings answering booking messages.

### How far in advance should you send appointment reminders?

One the day before and one an hour or two before suits most salon appointments. The first gives clients time to rebook; the second catches people who forgot.

### Can clients cancel or reschedule an online booking themselves?

In most booking tools, yes. In Systeme.io, the confirmation email includes buttons to reschedule or cancel, and you both get an email when a booking changes. Set a cancellation deadline so late changes still come to you.

## The short version

- Start with one booking event for your most booked service.
- Let AI draft the page description, then check every detail yourself.
- Book only the hours you want, and keep the default 24-hour and 1-hour reminders.
- Add buffer time and a daily limit so you are never booked back to back.
- Test it with your own booking before you share the link.
