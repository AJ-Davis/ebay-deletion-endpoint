# eBay Deletion Notification Endpoint

A simple Flask webhook endpoint to handle eBay account deletion notifications, required for eBay API compliance.

## Overview

This endpoint is required by eBay for applications that use their APIs. When a user deletes their eBay account, eBay will send a POST request to this endpoint to notify your application.

## Files

- `app.py` - Flask application with the deletion endpoint
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment configuration

## Deployment

This app is configured for deployment on Render.com:

1. Connect this repository to Render
2. Render will automatically detect the Python environment
3. The app will be deployed with the endpoint available at `/ebay/deletion`

## Endpoint

**POST** `/ebay/deletion`

Receives eBay account deletion notifications and logs them.

## Usage

Once deployed, register your endpoint URL with eBay in the Developer Portal under "Marketplace Account Deletion".

Example URL: `https://your-app.onrender.com/ebay/deletion`