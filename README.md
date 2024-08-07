# Flask SIA Scraper

A simple Flask application that scrapes student data and schedules from the [Mercu Buana University website](https://sia.mercubuana.ac.id) and serves the scraped data as an API.

## Features

- **Student Data Scraping**: Retrieve student information such as NIM, name, faculty, major, SKS, semester, and GPA.
- **Schedule Scraping**: Retrieve the class schedule for a given student.

## URL

The API is hosted at: [https://sia-mercubuana.api.altaf.xyz](https://sia-mercubuana.api.altaf.xyz)

## Endpoints

- **`/getStudentData`**: Accepts a POST request with JSON payload containing `nim` and `password`. Returns student data in JSON format.
- **`/getSchedule`**: Accepts a POST request with JSON payload containing `nim` and `password`. Returns the class schedule in JSON format.

## Copyright

© 2024 Naufal Altaf. All rights reserved.