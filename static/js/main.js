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