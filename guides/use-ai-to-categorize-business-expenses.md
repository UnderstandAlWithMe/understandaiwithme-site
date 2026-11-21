---
title: Use AI to Sort a Year of Business Expenses in an Afternoon
description: Export your bank transactions, let ChatGPT or Claude suggest expense categories, then check the result before it goes near your books or tax return.
date: 2026-11-17
tile: receipts-and-expenses
---
If your business spending sits in a bank account as hundreds of uncategorized lines, sorting it by hand is slow and dull. An AI assistant such as ChatGPT or Claude can do the first pass for you: read a spreadsheet of transactions, suggest a category for each line and flag the ones it is unsure about. You stay in charge of the final answer.

This guide shows a safe, repeatable way to do it. *We are not financial advisers.* AI suggestions are a starting point, not tax advice, so have your accountant or bookkeeper check anything you are unsure about.

## What AI is good at here (and what it is not)

AI is good at pattern work: recognizing that "AMZN Mktp" is probably office supplies, that a monthly charge from a software company is a subscription, or that the same fuel station appears every week. It is quick and consistent once you give it clear rules.

It is not good at knowing *why* you bought something. A restaurant bill could be client entertainment, a staff meal or a personal dinner, and the tax treatment can differ. It also does not know the rules in your country unless you check them. That is why every step below ends with a human review.

## Step-by-step: from bank export to categorized list

### 1. Export your transactions

Most business bank accounts and accounting tools let you download transactions as a CSV or Excel file. Pick one period, such as a quarter or a tax year. Keep only the columns you need: date, description, amount and (if present) reference.

### 2. Remove what the AI does not need to see

Before uploading, delete or mask account numbers, card numbers and anything that identifies customers personally. Check your AI tool's data settings too. Many paid business plans let you turn off use of your data for model training. If you would not email the file to a stranger, clean it first.

### 3. Write your category list

Give the AI a fixed list, ideally matching the categories in your accounting software or the ones your accountant uses. For example:

- Software and subscriptions
- Office supplies
- Travel
- Fuel and vehicle
- Advertising and marketing
- Professional fees
- Bank charges
- Personal or unclear

A fixed list stops the AI inventing new categories every time.

### 4. Use a clear prompt

Upload the file and paste something like this:

*"You are helping a small business sort its bank transactions. Add a column called Category, using only the categories in the list below. Add a column called Confidence with High, Medium or Low. If a transaction could be personal or you cannot tell what it is, use 'Personal or unclear' and Low. Do not change any dates or amounts. Return the result as a downloadable spreadsheet."*

Then paste your category list. If you have rules, add them: "Anything from [supplier name] is Software", "All fuel stations are Fuel and vehicle".

### 5. Review the Low and Medium lines yourself

Sort by the Confidence column. Work through every Low and Medium line and fix it. Then spot-check a handful of the High lines. If you see the same mistake twice, add a rule to your prompt and run it again.

### 6. Check the totals

Ask the AI to total each category, then compare the overall total with your bank export. They should match exactly. If they do not, a line was dropped or changed, so do not use that file.

### 7. Save your prompt for next time

Keep the prompt, the category list and your rules in a document, or in a Claude Project or custom GPT. Next month the job takes minutes, not an afternoon.

## Keep the receipts as well

Categorizing your bank lines does not replace keeping receipts and invoices. Tax authorities set their own record-keeping rules:

- **UK:** HMRC says self-employed people must keep records for at least 5 years after the 31 January submission deadline of the relevant tax year. See [GOV.UK: how long to keep your records](https://www.gov.uk/self-employed-records/how-long-to-keep-your-records).
- **Australia:** the ATO says you need to keep most business records for 5 years. See the [ATO record-keeping overview](https://www.ato.gov.au/businesses-and-organisations/preparing-lodging-and-paying/record-keeping-for-business/overview-of-record-keeping-rules-for-business).
- **US:** the period depends on your situation. See the [IRS recordkeeping guidance](https://www.irs.gov/businesses/small-businesses-self-employed/recordkeeping).

Elsewhere, check your local tax authority or government business site.

## Common mistakes to avoid

1. **Letting the AI decide what is tax-deductible.** Ask it to categorize, not to rule on deductions.
2. **Uploading raw files with account details.** Clean them first.
3. **Skipping the totals check.** It is the quickest way to catch a dropped row.
4. **Starting from scratch every month.** A saved prompt is what makes this a system.

## The short version

- Export one period of transactions as a spreadsheet and remove sensitive details.
- Give the AI a fixed category list and ask for a Confidence column.
- Review every Low and Medium line, spot-check the rest and make sure the totals match.
- Save your prompt and rules so next month is quick.
- Keep your receipts, and ask your accountant about anything unclear. We are not financial advisers.
