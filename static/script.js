document.addEventListener('DOMContentLoaded', function() {
    const passwordForm = document.getElementById('password-form');
    const passwordInput = document.getElementById('password');
    const togglePasswordBtn = document.getElementById('toggle-password');
    const analysisResults = document.getElementById('analysis-results');
    const copyHashBtn = document.getElementById('copy-hash');

    togglePasswordBtn.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        const icon = this.querySelector('i');
        icon.classList.toggle('fa-eye');
        icon.classList.toggle('fa-eye-slash');
    });

    passwordInput.addEventListener('input', function() {
        if (this.value.length > 0) {
            analyzePassword();
        } else {
            analysisResults.style.display = 'none';
        }
    });

    passwordForm.addEventListener('submit', function(e) {
        e.preventDefault();
        analyzePassword();
    });

    copyHashBtn.addEventListener('click', function() {
        const hashInput = document.getElementById('sha256-hash');
        hashInput.select();
        document.execCommand('copy');
        
        const icon = this.querySelector('i');
        const originalClass = icon.className;
        icon.className = 'fas fa-check';
        this.classList.add('btn-success');
        this.classList.remove('btn-outline-secondary');
        
        setTimeout(() => {
            icon.className = originalClass;
            this.classList.remove('btn-success');
            this.classList.add('btn-outline-secondary');
        }, 1500);
    });

    function analyzePassword() {
        const password = passwordInput.value;
        
        if (!password) {
            analysisResults.style.display = 'none';
            return;
        }

        fetch('/analyze_password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password: password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Analysis error:', data.error);
                return;
            }
            displayAnalysisResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function displayAnalysisResults(analysis) {
        analysisResults.style.display = 'block';

        const strengthBar = document.getElementById('strength-bar');
        const strengthLevel = document.getElementById('strength-level');
        const strengthScore = document.getElementById('strength-score');
        const entropyValue = document.getElementById('entropy-value');
        const sha256Hash = document.getElementById('sha256-hash');
        const patternsSection = document.getElementById('patterns-section');
        const patternsList = document.getElementById('patterns-list');
        const suggestionsList = document.getElementById('suggestions-list');

        strengthBar.style.width = analysis.score + '%';
        strengthBar.className = `progress-bar bg-${analysis.strength.color}`;
        
        strengthLevel.textContent = analysis.strength.level;
        strengthLevel.className = `badge bg-${analysis.strength.color}`;
        
        strengthScore.textContent = `${analysis.score}/100`;
        
        entropyValue.textContent = `${analysis.entropy} bits`;
        
        sha256Hash.value = analysis.sha256_hash;

        if (analysis.patterns && analysis.patterns.length > 0) {
            patternsSection.style.display = 'block';
            patternsList.innerHTML = '';
            analysis.patterns.forEach(pattern => {
                const badge = document.createElement('span');
                badge.className = 'badge bg-warning pattern-badge';
                badge.textContent = pattern.description;
                patternsList.appendChild(badge);
            });
        } else {
            patternsSection.style.display = 'none';
        }

        suggestionsList.innerHTML = '';
        if (analysis.suggestions && analysis.suggestions.length > 0) {
            analysis.suggestions.forEach(suggestion => {
                const li = document.createElement('li');
                li.className = 'suggestion-item';
                li.innerHTML = `<i class="fas fa-arrow-right me-2"></i>${suggestion}`;
                suggestionsList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.className = 'suggestion-item bg-success';
            li.innerHTML = '<i class="fas fa-check me-2"></i>Great! Your password looks strong.';
            suggestionsList.appendChild(li);
        }
    }
});
