let probabilityChart = null;

async function analyzeJob() {
    const jobDescription = document.getElementById('jobDescription').value.trim();
    
    if (!jobDescription) {
        alert('Please enter a job description first.');
        return;
    }
    
    // Show loading, hide results
    document.getElementById('loading').classList.remove('d-none');
    document.getElementById('results').classList.add('d-none');
    document.getElementById('analyzeBtn').disabled = true;
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ job_description: jobDescription })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResults(result);
        } else {
            throw new Error(result.error || 'Prediction failed');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        document.getElementById('loading').classList.add('d-none');
        document.getElementById('analyzeBtn').disabled = false;
    }
}

function displayResults(result) {
    // Show results section
    document.getElementById('results').classList.remove('d-none');
    
    // Update prediction text
    const predictionText = document.getElementById('predictionText');
    const resultHeader = document.getElementById('resultHeader');
    
    if (result.prediction === 1) {
        predictionText.innerHTML = '<i class="fas fa-exclamation-triangle"></i> FAKE JOB DETECTED';
        predictionText.className = 'text-danger fw-bold';
        resultHeader.className = 'card-header bg-danger text-white';
    } else {
        predictionText.innerHTML = '<i class="fas fa-check-circle"></i> LIKELY REAL JOB';
        predictionText.className = 'text-success fw-bold';
        resultHeader.className = 'card-header bg-success text-white';
    }
    
    // Update probability bars
    const realPercent = result.probabilities.real;
    const fakePercent = result.probabilities.fake;
    
    document.getElementById('realPercent').textContent = `${realPercent}% Real`;
    document.getElementById('fakePercent').textContent = `${fakePercent}% Fake`;
    
    document.getElementById('realBar').style.width = `${realPercent}%`;
    document.getElementById('realBar').textContent = `${realPercent}%`;
    
    document.getElementById('fakeBar').style.width = `${fakePercent}%`;
    document.getElementById('fakeBar').textContent = `${fakePercent}%`;
    
    // Update chart
    updateProbabilityChart(realPercent, fakePercent);
    
    // Update word cloud
    if (result.wordcloud) {
        document.getElementById('wordcloudImg').src = `data:image/png;base64,${result.wordcloud}`;
    }
    
    // Update red flags
    const redFlagsList = document.getElementById('redFlags');
    redFlagsList.innerHTML = '';
    
    if (result.red_flags && result.red_flags.length > 0) {
        result.red_flags.forEach(flag => {
            const li = document.createElement('li');
            li.className = 'list-group-item list-group-item-danger d-flex justify-content-between align-items-center';
            li.innerHTML = `
                ${flag[0]}
                <span class="badge bg-danger rounded-pill">${flag[1].toFixed(2)}</span>
            `;
            redFlagsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.className = 'list-group-item list-group-item-light';
        li.textContent = 'No suspicious words detected';
        redFlagsList.appendChild(li);
    }
    
    // Update green flags
    const greenFlagsList = document.getElementById('greenFlags');
    greenFlagsList.innerHTML = '';
    
    if (result.green_flags && result.green_flags.length > 0) {
        result.green_flags.forEach(flag => {
            const li = document.createElement('li');
            li.className = 'list-group-item list-group-item-success d-flex justify-content-between align-items-center';
            li.innerHTML = `
                ${flag[0]}
                <span class="badge bg-success rounded-pill">${Math.abs(flag[1]).toFixed(2)}</span>
            `;
            greenFlagsList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.className = 'list-group-item list-group-item-light';
        li.textContent = 'No professional words detected';
        greenFlagsList.appendChild(li);
    }
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function updateProbabilityChart(realPercent, fakePercent) {
    const ctx = document.getElementById('probabilityChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (probabilityChart) {
        probabilityChart.destroy();
    }
    
    // Create new chart
    probabilityChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Real Job', 'Fake Job'],
            datasets: [{
                data: [realPercent, fakePercent],
                backgroundColor: [
                    'rgba(46, 204, 113, 0.8)',
                    'rgba(231, 76, 60, 0.8)'
                ],
                borderColor: [
                    'rgba(46, 204, 113, 1)',
                    'rgba(231, 76, 60, 1)'
                ],
                borderWidth: 2,
                hoverOffset: 15
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            size: 14,
                            family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
                        },
                        padding: 20
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ${context.raw}%`;
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true,
                duration: 2000
            }
        }
    });
}

// Add Enter key support for textarea
document.getElementById('jobDescription').addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        analyzeJob();
    }
});

// Initialize with sample text
document.addEventListener('DOMContentLoaded', function() {
    // Add sample text for testing
    const sampleText = `We are looking for a motivated individual to join our team. This is a fully remote position with competitive salary and benefits. Requirements include excellent communication skills and 3+ years of experience in the field. The successful candidate will collaborate with cross-functional teams and contribute to strategic initiatives.`;
    document.getElementById('jobDescription').value = sampleText;
});