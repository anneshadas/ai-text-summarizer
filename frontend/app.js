// frontend/app.js

const API_URL = "http://localhost:8000/api";

// Word count live update
document.getElementById('inputText').addEventListener('input', function() {
    const words = this.value.trim() === '' ? 0 : this.value.trim().split(/\s+/).length;
    const counter = document.getElementById('wordCount');
    counter.textContent = words;
    counter.style.color = words < 50 || words > 1000 ? '#e53e3e' : '#48bb78';
});

// Toggle options based on method
document.getElementById('method').addEventListener('change', function() {
    const isAbstractive = this.value === 'abstractive';
    document.getElementById('abstractiveOptions').style.display = isAbstractive ? 'block' : 'none';
    document.getElementById('extractiveOptions').style.display = isAbstractive ? 'none' : 'block';
});

// Main summarize function
async function summarize() {

    const text = document.getElementById('inputText').value.trim();
    const method = document.getElementById('method').value;
    const maxLength = parseInt(document.getElementById('maxLength').value);
    const numSentences = parseInt(document.getElementById('numSentences').value);

    // Hide previous results
    document.getElementById('error').style.display = 'none';
    document.getElementById('resultCard').style.display = 'none';

    // Basic frontend validation
    if (!text) {
        showError("Please enter some text first.");
        return;
    }

    // Show loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('summarizeBtn').disabled = true;

    try {
        // Build request body
        const body = { text, method };
        if (method === 'abstractive') body.max_length = maxLength;
        if (method === 'extractive') body.num_sentences = numSentences;

        // Call API
        const response = await fetch(`${API_URL}/summarize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.detail || "Something went wrong.");
            return;
        }

        // Show results
        displayResults(data);

    } catch (err) {
        showError("Cannot connect to server. Make sure backend is running.");
    } finally {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('summarizeBtn').disabled = false;
    }
}

function displayResults(data) {
    document.getElementById('summaryText').textContent = data.summary;
    document.getElementById('originalWords').textContent = data.original_words;
    document.getElementById('summaryWords').textContent = data.summary_words;
    document.getElementById('compression').textContent = data.compression_ratio + '%';
    document.getElementById('methodUsed').textContent = data.method;
    document.getElementById('resultCard').style.display = 'block';
}

function showError(message) {
    const err = document.getElementById('error');
    err.textContent = message;
    err.style.display = 'block';
}