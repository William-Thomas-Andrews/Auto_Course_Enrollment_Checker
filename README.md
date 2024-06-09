# Auto_Course_Enrollment_Checker Project

## Problem:

I wanted to take a course at my college, but it was full. I kept checking if the course was open, but I got tired of doing that.

## Solution:

I used selenium with chrome driver and scheduler to every 5 minutes automatically enter the registration website and check the availablity of the course. If the seats open was still 0, the program did nothing and continued with the scheduler. If the seats open changed from 0, then the program sent a message to a Telegram API that sent me a message through a Telegram bot. In this message was the number of seats open. This program worked and it notified me when the course was available.

To run this code, you need to install chrome driver on your computer.
