// Handle download counter
function incrementDownloadCount() {
    fetch('/increment-downloads', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('download-count').textContent = data.count;
    })
    .catch(error => console.error('Error:', error));
}

// Increment view count on page load
window.onload = function() {
    fetch('/increment-views', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('view-count').textContent = data.count;
    })
    .catch(error => console.error('Error:', error));
}

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});