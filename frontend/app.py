import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="centered",
)


st.title("⚖️ LegalEase")

st.write(
    "AI-powered legal information assistant"
)

st.info(
    "LegalEase provides general legal information for educational "
    "purposes. It is not a substitute for professional legal advice."
)


language = st.selectbox(
    "Response Language",
    [
        "English",
        "Tamil",
        "Hindi",
    ],
)


question = st.text_area(
    "Enter your legal question",
    placeholder=(
        "Example: What are the basic steps involved "
        "in filing a consumer complaint?"
    ),
    height=160,
)


if st.button("Ask LegalEase", type="primary"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:

        with st.spinner("Generating response..."):

            try:

                response = requests.post(
                    f"{API_URL}/api/ask",
                    json={
                        "question": question,
                        "language": language,
                    },
                    timeout=120,
                )

                if response.status_code == 200:

                    data = response.json()

                    st.session_state["answer"] = data["answer"]
                    st.session_state["disclaimer"] = data[
                        "disclaimer"
                    ]

                else:

                    st.error(
                        f"API Error: {response.text}"
                    )

            except requests.exceptions.RequestException as exc:

                st.error(
                    "Could not connect to the LegalEase backend.\n\n"
                    f"{exc}"
                )


if "answer" in st.session_state:

    st.divider()

    st.subheader("Answer")

    st.markdown(
        st.session_state["answer"]
    )

    st.caption(
        st.session_state["disclaimer"]
    )

    st.divider()

    st.subheader("Export Response")

    export_title = "LegalEase Response"
    export_content = st.session_state["answer"]

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("Create TXT"):

            try:

                response = requests.post(
                    f"{API_URL}/api/export/txt",
                    json={
                        "title": export_title,
                        "content": export_content,
                    },
                    timeout=30,
                )

                if response.ok:

                    st.download_button(
                        "Download TXT",
                        data=response.content,
                        file_name="legalease_response.txt",
                        mime="text/plain",
                    )

            except requests.RequestException as exc:

                st.error(str(exc))

    with col2:

        if st.button("Create DOCX"):

            try:

                response = requests.post(
                    f"{API_URL}/api/export/docx",
                    json={
                        "title": export_title,
                        "content": export_content,
                    },
                    timeout=30,
                )

                if response.ok:

                    st.download_button(
                        "Download DOCX",
                        data=response.content,
                        file_name="legalease_response.docx",
                        mime=(
                            "application/vnd.openxmlformats-officedocument."
                            "wordprocessingml.document"
                        ),
                    )

            except requests.RequestException as exc:

                st.error(str(exc))

    with col3:

        if st.button("Create PDF"):

            try:

                response = requests.post(
                    f"{API_URL}/api/export/pdf",
                    json={
                        "title": export_title,
                        "content": export_content,
                    },
                    timeout=30,
                )

                if response.ok:

                    st.download_button(
                        "Download PDF",
                        data=response.content,
                        file_name="legalease_response.pdf",
                        mime="application/pdf",
                    )

            except requests.RequestException as exc:

                st.error(str(exc))