#!/bin/bash

# Nova Act Automation Test Script
# Easy test-clean-repeat cycle for development

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project paths
PROJECT_ROOT="/Users/marzuqq/Documents/Nova-Act-POC-"
DOCKER_DIR="$PROJECT_ROOT/docker"
DATA_DIR="$PROJECT_ROOT/data"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if we're in the right directory
check_directory() {
    if [[ ! -d "$PROJECT_ROOT" ]]; then
        print_error "Project directory not found: $PROJECT_ROOT"
        exit 1
    fi
    
    if [[ ! -d "$DOCKER_DIR" ]]; then
        print_error "Docker directory not found: $DOCKER_DIR"
        exit 1
    fi
}

# Function to show current automation mode
show_current_mode() {
    cd "$DOCKER_DIR"
    current_mode=$(grep "USE_MANUAL_FILLING=" .env | cut -d'=' -f2)
    if [[ "$current_mode" == "true" ]]; then
        print_status "Current mode: MANUAL form filling"
    else
        print_status "Current mode: AUTO-FILL (JSON upload)"
    fi
}

# Function to switch automation mode
switch_mode() {
    cd "$DOCKER_DIR"
    current_mode=$(grep "USE_MANUAL_FILLING=" .env | cut -d'=' -f2)
    
    if [[ "$current_mode" == "true" ]]; then
        # Switch to auto-fill mode
        sed -i '' 's/USE_MANUAL_FILLING=true/USE_MANUAL_FILLING=false/' .env
        print_success "Switched to AUTO-FILL mode (JSON upload)"
    else
        # Switch to manual mode
        sed -i '' 's/USE_MANUAL_FILLING=false/USE_MANUAL_FILLING=true/' .env
        print_success "Switched to MANUAL form filling mode"
    fi
}

# Function to run automation
run_automation() {
    show_current_mode
    print_status "Starting Nova Act automation..."
    cd "$DOCKER_DIR"
    
    # Check if .env exists
    if [[ ! -f ".env" ]]; then
        print_error ".env file not found in $DOCKER_DIR"
        print_warning "Please create .env file from docker.env.template"
        exit 1
    fi
    
    # Run automation
    docker-compose up nova-act-automation
    
    # Check exit code
    if [[ $? -eq 0 ]]; then
        print_success "Automation completed successfully!"
        return 0
    else
        print_error "Automation failed!"
        return 1
    fi
}

# Function to show results
show_results() {
    print_status "Showing automation results..."
    
    # Show latest results file
    latest_result=$(ls -t "$DATA_DIR/results/automation_results_"*.json 2>/dev/null | head -1)
    if [[ -n "$latest_result" ]]; then
        print_success "Latest result: $(basename "$latest_result")"
        echo "----------------------------------------"
        cat "$latest_result" | python3 -m json.tool 2>/dev/null || cat "$latest_result"
        echo "----------------------------------------"
    else
        print_warning "No results files found"
    fi
    
    # Show submissions
    submission_count=$(ls -1 "$DATA_DIR/submissions/"*.json 2>/dev/null | wc -l)
    print_status "Total submissions: $submission_count"
    
    # Show uploads
    upload_count=$(ls -1 "$DATA_DIR/uploads/"*.json 2>/dev/null | wc -l)
    print_status "Total uploads: $upload_count"
}

# Function to clean up
clean_up() {
    print_status "Cleaning up..."
    
    # Stop and remove containers
    cd "$DOCKER_DIR"
    docker-compose down
    
    # Clean up data files
    print_status "Removing results, submissions, and uploads..."
    rm -f "$DATA_DIR/results/automation_results_"*.json
    rm -f "$DATA_DIR/submissions/"*.json
    rm -f "$DATA_DIR/uploads/"*.json
    
    # Optional: Clean up Docker images
    read -p "Clean up Docker images to save space? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleaning up Docker images..."
        docker system prune -f
    fi
    
    print_success "Cleanup completed!"
}

# Function to ask for user input
ask_yes_no() {
    while true; do
        read -p "$1 (y/N): " -n 1 -r
        echo
        case $REPLY in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) return 1;;
        esac
    done
}

# Main loop
main() {
    check_directory
    
    print_status "Nova Act Automation Test Script"
    print_status "================================"
    
    while true; do
        echo
        show_current_mode
        echo
        print_status "Options:"
        echo "1. Run automation"
        echo "2. Show results"
        echo "3. Clean up"
        echo "4. Switch automation mode"
        echo "5. Run → Show → Clean (full cycle)"
        echo "6. Exit"
        echo
        
        read -p "Choose option (1-6): " -n 1 -r
        echo
        
        case $REPLY in
            1)
                run_automation
                ;;
            2)
                show_results
                ;;
            3)
                clean_up
                ;;
            4)
                switch_mode
                ;;
            5)
                print_status "Running full test cycle..."
                if run_automation; then
                    show_results
                    echo
                    if ask_yes_no "Clean up results?"; then
                        clean_up
                    fi
                    echo
                    if ask_yes_no "Run another test?"; then
                        continue
                    else
                        break
                    fi
                fi
                ;;
            6)
                print_status "Exiting..."
                exit 0
                ;;
            *)
                print_error "Invalid option. Please choose 1-6."
                ;;
        esac
    done
}

# Run main function
main "$@" 