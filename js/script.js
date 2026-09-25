// =====================================================
// BACKEND API CONFIGURATION
// =====================================================

const API_BASE_URL =
    "https://tgsrtc-complaint-backend.onrender.com";
// =====================================================
// MOBILE MENU
// =====================================================

const menuButton =
    document.getElementById("menuButton");

const navLinks =
    document.getElementById("navLinks");

if (menuButton && navLinks) {

    menuButton.addEventListener("click", () => {

        navLinks.classList.toggle("show");

    });

}
// =====================================================
// COMPLAINT FORM SUBMISSION
// =====================================================

const complaintForm = document.getElementById("complaintForm");

if (complaintForm) {

    complaintForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        // Disable submit button while sending
        const submitButton = complaintForm.querySelector(
            'button[type="submit"]'
        );

        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = "Submitting...";
        }


        // =====================================================
        // COLLECT FORM DATA
        // =====================================================

        const formData = new FormData();

        formData.append(
            "name",
            document.getElementById("name").value.trim()
        );

        formData.append(
            "mobile",
            document.getElementById("mobile").value.trim()
        );

        formData.append(
            "email",
            document.getElementById("email").value.trim()
        );

        formData.append(
            "bus_number",
            document.getElementById("busNumber").value.trim()
        );

        formData.append(
            "journey_date",
            document.getElementById("journeyDate").value
        );

        formData.append(
            "journey_time",
            document.getElementById("journeyTime").value
        );

        formData.append(
            "route",
            document.getElementById("route").value.trim()
        );

        formData.append(
            "boarding_point",
            document.getElementById("boardingPoint").value.trim()
        );

        formData.append(
            "destination",
            document.getElementById("destination").value.trim()
        );

        formData.append(
            "category",
            document.getElementById("category").value
        );

        formData.append(
            "description",
            document.getElementById("description").value.trim()
        );


        // =====================================================
        // ADD SUPPORTING EVIDENCE
        // =====================================================

        const evidenceInput =
            document.getElementById("evidence");

        if (
            evidenceInput &&
            evidenceInput.files &&
            evidenceInput.files.length > 0
        ) {

            formData.append(
                "evidence",
                evidenceInput.files[0]
            );

        }


        try {

            // =====================================================
            // SEND COMPLAINT TO FASTAPI BACKEND
            // =====================================================

            const response = await fetch(
    `${API_BASE_URL}/api/complaints`,
                {
                    method: "POST",

                    // IMPORTANT:
                    // Do NOT manually set Content-Type.
                    // Browser automatically creates multipart/form-data.
                    body: formData
                }
            );


            // =====================================================
            // CHECK SERVER RESPONSE
            // =====================================================

            if (!response.ok) {

    const text = await response.text();   // ✅ read ONLY once

    console.error("SERVER ERROR:", text);

    alert("Error from server:\n" + text);

    throw new Error(text);
}

            // =====================================================
            // GET RESPONSE FROM BACKEND
            // =====================================================

            const result =
                await response.json();


            // =====================================================
            // SAVE FOR FRONTEND TRACKING
            // =====================================================

            const complaint = {

                complaint_id:
                    result.complaint_id,

                name:
                    document.getElementById("name")
                        .value.trim(),

                mobile:
                    document.getElementById("mobile")
                        .value.trim(),

                email:
                    document.getElementById("email")
                        .value.trim() || null,

                bus_number:
                    document.getElementById("busNumber")
                        .value.trim(),

                journey_date:
                    document.getElementById("journeyDate")
                        .value,

                journey_time:
                    document.getElementById("journeyTime")
                        .value || null,

                route:
                    document.getElementById("route")
                        .value.trim() || null,

                boarding_point:
                    document.getElementById("boardingPoint")
                        .value.trim(),

                destination:
                    document.getElementById("destination")
                        .value.trim(),

                category:
                    document.getElementById("category")
                        .value,

                description:
                    document.getElementById("description")
                        .value.trim(),

                status:
                    result.status,

                evidence_file:
                    result.evidence_file || null,

                submitted_at:
                    new Date().toLocaleString()
            };


            localStorage.setItem(
                "latestComplaint",
                JSON.stringify(complaint)
            );


            // =====================================================
            // SHOW SUCCESS SCREEN
            // =====================================================

            showComplaintSuccess(
                result.complaint_id
            );


        } catch (error) {

    console.error(
        "Complaint submission error:",
        error
    );

    alert("Submission failed:\n" + error.message);

    // Re-enable button
    if (submitButton) {

        submitButton.disabled = false;

        submitButton.textContent =
            "Submit Complaint";

    }
}


    });
}
// =====================================================
// SUCCESS SCREEN
// =====================================================

function showComplaintSuccess(complaintId) {

    const container = document.querySelector(
        ".complaint-container"
    );

    if (!container) {
        return;
    }


    container.innerHTML = `

        <div class="success-box">

            <div class="success-icon">
                ✓
            </div>

            <h2>
                Complaint Submitted Successfully
            </h2>

            <p>
                Thank you for submitting your complaint.
                Your complaint has been recorded in this prototype.
            </p>

            <div class="complaint-id-box">

                <span>
                    Your Complaint ID
                </span>

                <strong id="generatedComplaintId">
                    ${complaintId}
                </strong>

            </div>

            <div class="success-actions">

                <button
                    type="button"
                    class="btn primary-btn"
                    onclick="copyComplaintId()"
                >
                    Copy Complaint ID
                </button>

                <a
                    href="track.html"
                    class="btn secondary-btn"
                >
                    Track Complaint
                </a>

                <a
                    href="../index.html"
                    class="btn outline-btn"
                >
                    Back to Home
                </a>

            </div>

        </div>

    `;
}


// =====================================================
// COPY COMPLAINT ID
// =====================================================

function copyComplaintId() {

    const complaintIdElement =
        document.getElementById(
            "generatedComplaintId"
        );

    if (!complaintIdElement) {
        return;
    }


    const complaintId =
        complaintIdElement.textContent.trim();


    if (
        navigator.clipboard &&
        window.isSecureContext
    ) {

        navigator.clipboard
            .writeText(complaintId)
            .then(() => {

                alert(
                    "Complaint ID copied successfully!"
                );

            })
            .catch(() => {

                alert(
                    "Complaint ID: " + complaintId
                );

            });

    } else {

        alert(
            "Complaint ID: " + complaintId
        );

    }

}