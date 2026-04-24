document.addEventListener('DOMContentLoaded', function() {
    const checkEligibilityBtn = document.getElementById('check-eligibility-btn');
    const resultsSection = document.getElementById('results-section');
    const resultsContainer = document.getElementById('results');

    if (checkEligibilityBtn) {
        checkEligibilityBtn.addEventListener('click', function() {
            // Show loading state
            this.textContent = 'Finding schemes...';
            this.disabled = true;
            
            // Make request to check eligibility
            fetch('/check_eligibility', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                
                displaySchemes(data.schemes, data.user_name);
                resultsSection.style.display = 'block';
                resultsSection.scrollIntoView({ behavior: 'smooth' });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to check eligibility. Please try again.');
            })
            .finally(() => {
                // Reset button state
                this.textContent = 'Find My Schemes';
                this.disabled = false;
            });
        });
    }
});

function displaySchemes(schemes, userName) {
    const results = document.getElementById('results');
    results.innerHTML = '';

    if (schemes.length === 0) {
        results.innerHTML = `<p>Sorry ${userName}, no schemes found for your details.</p>`;
        return;
    }

    const greeting = document.createElement("h3");
    greeting.textContent = `Hello ${userName}, here are the schemes you are eligible for:`;
    greeting.style.color = '#faf9ff';
    greeting.style.textAlign = 'center';
    greeting.style.marginBottom = '30px';
    results.appendChild(greeting);

    schemes.forEach(scheme => {
        const card = document.createElement("div");
        card.className = "scheme-card";
        
        const saveButtonText = scheme.is_saved ? 'Saved ✓' : 'Save';
        const saveButtonClass = scheme.is_saved ? 'unsave-scheme-btn' : 'save-scheme-btn';
        const saveButtonAction = scheme.is_saved ? 'unsave' : 'save';
        
        card.innerHTML = `
            <h3>${scheme.name}</h3>
            <p>${scheme.description}</p>
            <p><strong>Eligibility:</strong> ${scheme.eligibility}</p>
            <div class="scheme-actions">
                <button class="${saveButtonClass}" 
                        data-scheme='${JSON.stringify(scheme)}'
                        data-action="${saveButtonAction}">
                    ${saveButtonText}
                </button>
            </div>
        `;
        results.appendChild(card);
    });

    // Add event listeners for save/unsave buttons
    addSaveButtonListeners();
}

function addSaveButtonListeners() {
    const saveButtons = document.querySelectorAll('.save-scheme-btn, .unsave-scheme-btn');
    
    saveButtons.forEach(button => {
        button.addEventListener('click', function() {
            const scheme = JSON.parse(this.getAttribute('data-scheme'));
            const action = this.getAttribute('data-action');
            
            // Disable button during request
            const originalText = this.textContent;
            this.textContent = action === 'save' ? 'Saving...' : 'Removing...';
            this.disabled = true;
            
            const endpoint = action === 'save' ? '/save_scheme' : '/remove_scheme';
            
            fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: scheme.name,
                    description: scheme.description,
                    eligibility: scheme.eligibility
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    // Success - update button state
                    if (action === 'save') {
                        this.textContent = 'Saved ✓';
                        this.className = 'unsave-scheme-btn';
                        this.setAttribute('data-action', 'unsave');
                    } else {
                        this.textContent = 'Save Scheme';
                        this.className = 'save-scheme-btn';
                        this.setAttribute('data-action', 'save');
                    }
                    
                    // Show success message
                    showToast(data.message, 'success');
                } else {
                    // Error
                    this.textContent = originalText;
                    showToast(data.error || 'Operation failed', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.textContent = originalText;
                showToast('Operation failed. Please try again.', 'error');
            })
            .finally(() => {
                this.disabled = false;
            });
        });
    });
}

function showToast(message, type) {
    // Simple toast notification
    const toast = document.createElement('div');
    toast.className = `flash-message flash-${type}`;
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '1000';
    toast.style.maxWidth = '300px';
    toast.innerHTML = `
        ${message}
        <button type="button" class="flash-close" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    document.body.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 5000);
}
