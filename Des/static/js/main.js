// Main JavaScript for University Attendance System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize loading screen
    initLoadingScreen();
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize attendance marking functionality
    initAttendanceMarking();
    
    // Initialize form animations
    initFormAnimations();
    
    // Update clock
    updateClock();
    setInterval(updateClock, 1000);
});

// Loading Screen Management
function initLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    
    if (loadingScreen) {
        // Hide loading screen after 2.5 seconds
        setTimeout(() => {
            loadingScreen.style.opacity = '0';
            loadingScreen.style.visibility = 'hidden';
        }, 2500);
    }
}

// Initialize Bootstrap tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Attendance Marking Functionality
function initAttendanceMarking() {
    const attendanceCheckboxes = document.querySelectorAll('.attendance-checkbox');
    
    attendanceCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const studentId = this.getAttribute('data-student-id');
            const status = this.checked ? 'present' : 'absent';
            
            // Update the status display
            updateAttendanceStatus(studentId, status);
        });
    });
}

// Update attendance status display
function updateAttendanceStatus(studentId, status) {
    const statusElement = document.querySelector(`[data-status-id="${studentId}"]`);
    if (statusElement) {
        statusElement.className = `badge badge-${status}`;
        statusElement.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    }
}

// Form Animations
function initFormAnimations() {
    const formElements = document.querySelectorAll('.form-control, .btn');
    
    formElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        element.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

// Success Message Display
function showSuccessMessage(message) {
    const alertContainer = document.createElement('div');
    alertContainer.className = 'alert alert-success alert-dismissible fade show';
    alertContainer.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    insertAlert(alertContainer);
}

// Error Message Display
function showErrorMessage(message) {
    const alertContainer = document.createElement('div');
    alertContainer.className = 'alert alert-danger alert-dismissible fade show';
    alertContainer.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    insertAlert(alertContainer);
}

// Insert alert into page
function insertAlert(alertElement) {
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertElement, container.firstChild);
        
        // Auto-remove alert after 5 seconds
        setTimeout(() => {
            if (alertElement.parentNode) {
                alertElement.remove();
            }
        }, 5000);
    }
}

// Real-time clock
function updateClock() {
    const clockElement = document.getElementById('current-time');
    if (clockElement) {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        const dateString = now.toLocaleDateString();
        clockElement.innerHTML = `
            <i class="fas fa-clock me-2"></i>
            ${timeString} | ${dateString}
        `;
    }
}

// Print functionality
function printPage() {
    window.print();
}

// Download QR Code
function downloadQRCode() {
    const qrImage = document.querySelector('.qr-code img');
    if (qrImage) {
        const link = document.createElement('a');
        link.download = 'qr-code.png';
        link.href = qrImage.src;
        link.click();
    }
} 