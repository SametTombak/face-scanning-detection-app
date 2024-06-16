document.addEventListener("DOMContentLoaded", () => {
    const addFaceForm = document.getElementById("addFaceForm");
    const faceTableBody = document.getElementById("faceTableBody");

    const fetchFaces = async () => {
        const response = await fetch("/faces");
        const faces = await response.json();
        faceTableBody.innerHTML = faces.map(face => `
            <tr>
                <td>${face.id}</td>
                <td>${face.name}</td>
                <td>${face.role}</td>
                <td><img src="/static/images/${face.image_path}" alt="${face.name}" width="200"></td>
                <td>
                    <button class="btn btn-primary" onclick="editFace(${face.id})">Edit</button>
                    <button class="btn btn-danger" onclick="deleteFace(${face.id})">Delete</button>
                </td>
            </tr>
        `).join('');
    };

    addFaceForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(addFaceForm);
        if (document.getElementById("id").value != '') {
            await fetch("/update_face/" + document.getElementById("id").value, {
                method: "POST",
                body: formData
            });
            document.getElementById("id").value = null;
        }
        else {
            await fetch("/add_face", {
                method: "POST",
                body: formData
            });
        }
        addFaceForm.reset();
        fetchFaces();
    });

    window.editFace = async (id) => {
        const face = await fetch(`/get_face/${id}`).then(res => res.json());
        document.getElementById("id").value = face.id;
        document.getElementById("name").value = face.name;
        document.getElementById("role").value = face.role;
    };

    window.deleteFace = async (id) => {
        await fetch(`/delete_face/${id}`, {
            method: "DELETE"
        });
        fetchFaces();
    };

    fetchFaces();
});
