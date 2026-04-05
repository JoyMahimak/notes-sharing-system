function upload() {
    const fileInput = document.getElementById("fileInput");
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadNotes();
    })
    .catch(err => alert("Upload failed: " + err));
}

function loadNotes() {
    fetch("http://127.0.0.1:5000/notes")
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById("notesList");
        list.innerHTML = "";

        data.forEach(file => {
            const li = document.createElement("li");

            const link = document.createElement("a");
            link.href = "http://127.0.0.1:5000/download/" + file;
            link.textContent = file;

            li.appendChild(link);
            list.appendChild(li);
        });
    });
}

window.onload = loadNotes;