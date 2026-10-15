import streamlit as st
from PIL import Image


@st.dialog("Capture or upload Photo")
def add_photos_dialog():
    st.write("Add classroom photos to scan for attendance")

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    t1, t2 = st.columns(2)

    with t1:
        type_camera = "primary" if st.session_state.photo_tab == "camera" else "tertiary"
        if st.button("Camera", type=type_camera, width="stretch"):
            st.session_state.photo_tab = "camera"
            st.rerun()

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == "upload" else "tertiary"
        if st.button("Upload Photos", type=type_upload, width="stretch"):
            st.session_state.photo_tab = "upload"
            st.rerun()

    if st.session_state.photo_tab == "camera":
        cam_photo = st.camera_input("Take snapshot", key="dialog_cam")

        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast("Photo Captured")
            st.rerun()

    if st.session_state.photo_tab == "upload":
        upload_files = st.file_uploader(
            "Choose image files",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=True,
            key="dialog_upload"
        )

        if upload_files:
            for f in upload_files:
                st.session_state.attendance_images.append(Image.open(f))

            st.toast("Photos uploaded successfully")
            st.rerun()

    st.divider()

    if st.session_state.attendance_images:
        st.markdown("## Added Photos")

        cols = st.columns(3)

        for i, image in enumerate(st.session_state.attendance_images):
            with cols[i % 3]:
                st.image(image, width="stretch")
                st.caption(f"Photo {i + 1}")

    st.divider()

    if st.button("Done", type="primary", width="stretch"):
        st.rerun()