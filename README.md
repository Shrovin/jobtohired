# JobToHired

JobToHired is a live job-market research project that finds out what really gets people hired today. It combines a survey I designed and collect myself with a cloud data pipeline, AI analysis of written answers, and a Power BI dashboard.

## The problem

Finding a job is harder than ever. People apply to hundreds of roles, earn certifications and keep upskilling, yet nobody really knows which of these efforts actually lead to an offer. JobToHired compares what job seekers believe gets them hired with what recruiters actually value, and which channels (referrals, LinkedIn, job boards, cold emails) really work.

## How it works

Survey (Google Forms) → cloud pipeline (Azure) → data cleaning and quality checks (PySpark) → AI analysis of open-text answers → Power BI dashboard

Details of each step will be added as the project is built.

## Take the survey

It's anonymous and takes about 3 minutes: [Take the survey](https://forms.gle/eSy4wWhVpZFVFHFP8)

## Privacy

The survey is anonymous: no names, emails or company names are collected. Raw responses are never stored in this repository.

## Status

- ✅ Step 1: Survey designed, tested and live
- ⏳ Step 2: Cloud ingestion
- ⏳ Step 3: Data pipeline
- ⏳ Step 4: Power BI dashboard
- ⏳ Step 5: AI analysis
