function previewAudio(input, audioElementId) {
    const file = input.files[0];
    if (file) {
        const audioElement = document.getElementById(audioElementId);
        audioElement.src = URL.createObjectURL(file);
        audioElement.style.display = 'block';
    }
}

function submitForm() {
    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);

    fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('File paths and mic links:', data);
        alert(`Direction: ${data.Direction}`);
        let loudMic = document.querySelector(`#mic${data.index+1} img`);
        if (loudMic) 
            loudMic.src = "image2.png"; 
    }
    )
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while uploading the files.');
    });
}

