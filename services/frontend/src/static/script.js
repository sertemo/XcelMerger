document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('error-message');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(loginForm);
            const username = formData.get('username');
            const password = formData.get('password');

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `username=${username}&password=${password}`,
                });

                if (response.ok) {
                    window.location.href = "/upload";
                } else {
                    const errorText = await response.text();
                    errorMessage.textContent = errorText;
                    errorMessage.style.display = 'block';
                }
            } catch (error) {
                errorMessage.textContent = "An error occurred. Please try again.";
                errorMessage.style.display = 'block';
            }
        });
    }

    if (window.location.pathname === "/upload") {
        const dropArea = document.getElementById('drag-area');
        const fileInput = document.getElementById('fileElem');
        const fileSelectLink = document.getElementById('fileSelectLink');
        const fileList = document.getElementById('file-list');
        const addButton = document.getElementById('add-btn');
        const clearButton = document.getElementById('clearBtn');
        const downloadButton = document.getElementById('download-btn');
        const message = document.getElementById('error-message');
        const fileCount = document.getElementById('file-count');
        const fileSize = document.getElementById('file-size');
        let files = [];

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
        });

        dropArea.addEventListener('drop', handleDrop, false);
        fileInput.addEventListener('change', (e) => {
            handleFiles(e.target.files);
        });

        fileSelectLink.addEventListener('click', (e) => {
            e.preventDefault();
            fileInput.click();
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        function handleDrop(e) {
            let dt = e.dataTransfer;
            let droppedFiles = dt.files;
            handleFiles(droppedFiles);
        }

        function handleFiles(filesToHandle) {
            message.style.display = 'none'; // Ocultar el mensaje de error cuando se agregan archivos
            [...filesToHandle].forEach(file => {
                if (file.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" || file.type === "application/vnd.ms-excel") {
                    files.push(file);
                } else {
                    message.textContent = 'Solo se permiten archivos de Excel.';
                    message.style.display = 'block';
                }
            });
            updateFileList();
        }

        function updateFileList() {
            fileList.innerHTML = '';
            files.forEach((file, index) => {
                const li = document.createElement('li');
                li.textContent = file.name;

                const removeButton = document.createElement('button');
                removeButton.textContent = 'Eliminar';
                removeButton.addEventListener('click', () => {
                    files.splice(index, 1);
                    updateFileList();
                });

                li.appendChild(removeButton);
                fileList.appendChild(li);
            });
            clearButton.style.display = files.length > 1 ? 'inline-block' : 'none';
            updateFileInfo();
        }

        clearButton.addEventListener('click', () => {
            files = [];
            updateFileList();
        });

        addButton.addEventListener('click', () => {
            alert('Add button clicked');
        });

        downloadButton.addEventListener('click', () => {
            alert('Download button clicked');
        });

        function updateFileInfo() {
            fileCount.textContent = `Archivos subidos: ${files.length}`;
            let totalSize = files.reduce((acc, file) => acc + file.size, 0);
            fileSize.textContent = `Tamaño total: ${(totalSize / (1024 * 1024)).toFixed(2)} MB`;
        }
    }
});
