![Open in Codespaces](https://classroom.github.com/assets/open-in-codespaces-abfff4d4e15f9e1bd8274d9a39a0befe03a0632bb0f153d0ec72ff541cedbe34.svg)
# BTP405 Fall 2022: Project 1 - Due November 6 (25\%)

## Learning Objectives

* identify a potential product and feature set based on customer need
* apply agile methodologies to management of a software product
* create a high level architecture for a given product
* build a system given a high level architecture  

## Overview
Your task is to build a product that will assist a company with concert ticket sales management.  Users will have the opportunity to place orders for concert tickets. The following is information obtained when doing domain analysis and user research.  Use this as a starting point when designing your product. The agile product engineering approach should be used to manage your development. 

Your team can contain up to four members.  Each is expected to contribute equally to the final deliverable.

## Research

The solution must support multiple venues and multiple concerts in order to be useful to potential customers.  Each venue will have a unique seating plan.  For simplicity, the product will not track individual seats, but types of seats.  Each seat type will have a certain number of seats allocated to it.

For example, the "Toronto Concert Hall" may have 100 floor seats, 500 level 1 seats, and 3000 level 2 seats while the "Sony Centre" may have 1000 gold seats and 7000 silver seats.

Concerts are usually held on a particular date and at a particular venue.  A concert booked at a particular venue can (but does not have to) use all the seats in a venue.  A concert promoter may decide to only use 50% of the seats in the chosen venue. Each seat type is assigned a single price.  The number of seats sold shall be tracked by the system. 

Information about venues, concerts, pricing and initial account balances must be uploaded into the system. The information must be updatable by the company hosting the system

Our system should be able to accept and process tickets orders from *consumers* (who may purchase a small number of tickets) and *resellers* or other *commercial clients* that purchase tickets in bulk.  Such orders should be accepted via conventional Internet standards. It shall be able to process requests from multiple clients concurrently. 

For now, we can safely assume that users will communicate in English and make purchases in Canadian dollars. In order for the product to be used in multiple countries, it should be designed in a matter such that it can easily support other languages and currencies in the future.

Our current team has background using the Python language and its associated web frameworks.  Examples of these frameworks include [Django]{https://www.djangoproject.com/} and  [Flask]{https://flask.palletsprojects.com/en/2.2.x/}.  They also have experience with socket-level programming. 

## Deliverables

* a product vision
* personas, user stories, features
* a high architecture diagram
* your JIRA project, this should contain your item backlog and sprints
* a running product
* test approach
* a verbal discussion about your project with the instructor

## Grading Criteria 

Your work will be evaluated based on how well you have applied the concepts explored in the course material.  
