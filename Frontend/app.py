import os
from datetime import date
from html import escape

import requests
import streamlit as st

from dotenv import load_dotenv

from document_utils.docx_generator import (
    format_docx
)

from document_utils.pdf_generator import (
    format_pdf
)

from document_utils.txt_generator import (
    format_txt
)

from document_utils.sanitize import (
    sanitize_text
)


load_dotenv()


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT_SECONDS",
        "120"
    )
)


# -----------------------------
# CSS
# -----------------------------

st.markdown(
    """
<style>

.main-title {
    text-align: center;
    margin-bottom: 0.1rem;
}

.subtitle {
    text-align: center;
    color: #777;
    margin-bottom: 1.5rem;
}

.preview {
    background: #151515;
    color: #f5f5f5;
    padding: 1.25rem;
    border-radius: 12px;
    min-height: 300px;
    max-height: 650px;
    overflow-y: auto;
    font-family: Georgia,
                 "Times New Roman",
                 serif;
    line-height: 1.6;
}

</style>
""",
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<h1 class="main-title">'
    '⚖️ LegalEase'
    '</h1>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)


st.info(
    "LegalEase creates AI-assisted document "
    "drafts. Review the output with a qualified "
    "legal professional before relying on it "
    "for a real legal matter."
)


# -----------------------------
# Session State
# -----------------------------

if "document" not in st.session_state:

    st.session_state.document = ""


if "generated_type" not in st.session_state:

    st.session_state.generated_type = ""


# -----------------------------
# Input Form
# -----------------------------

with st.form(
    "document_form"
):

    left, right = st.columns(
        2
    )

    with left:

        document_type = st.text_input(
            "Document Type",
            placeholder=(
                "Freelance Work Contract"
            )
        )

        parties = st.text_area(
            "Parties Involved",
            placeholder=(
                "Jane Doe "
                "(Service Provider), "
                "TechNova Inc. "
                "(Client)"
            ),
            height=130
        )

    with right:

        effective_date = st.date_input(
            "Effective Date",
            value=date.today(),
            format="DD/MM/YYYY"
        )

        terms = st.text_area(
            "Terms & Conditions",
            placeholder=(
                "Payment to be made within "
                "30 days of invoice;\n"
                "Confidentiality must be "
                "maintained at all times;\n"
                "Either party may terminate "
                "with 15 days notice"
            ),
            height=130
        )
    submitted = st.form_submit_button(
        "✨ Generate Document",
        type="primary",
        use_container_width=True
    )


# -----------------------------
# Generate
# -----------------------------

if submitted:

    if not document_type.strip():

        st.error(
            "Please enter the document type."
        )

    elif not parties.strip():

        st.error(
            "Please enter the parties."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms."
        )

    else:

        normalized_terms = (
            terms.replace("\n", ";")
        )

        payload = {

            "document_type":
                document_type.strip(),

            "parties":
                parties.strip(),

            "terms":
                normalized_terms.strip(),

            "dates":
                effective_date.strftime(
                    "%B %d, %Y"
                )
        }

        with st.spinner(
            "Generating your document with Gemini..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=TIMEOUT
                )

                response.raise_for_status()

                data = response.json()

                st.session_state.document = (
                    sanitize_text(
                        data["content"]
                    )
                )

                st.session_state.generated_type = (
                    document_type.strip()
                )

                st.success(
                    "Document generated successfully."
                )

            except requests.RequestException as exc:

                detail = ""

                if getattr(
                    exc,
                    "response",
                    None
                ) is not None:

                    try:

                        detail = (
                            exc.response
                            .json()
                            .get(
                                "detail",
                                ""
                            )
                        )

                    except Exception:

                        detail = (
                            exc.response
                            .text[:500]
                        )

                st.error(
                    "Could not reach the "
                    "LegalEase backend.\n\n"
                    f"Make sure FastAPI is running "
                    f"at {BACKEND_URL}.\n\n"
                    f"{detail}"
                )


# -----------------------------
# Document Preview
# -----------------------------

if st.session_state.document:

    st.divider()

    st.subheader(
        "📄 Document Preview"
    )

    preview_text = escape(
        st.session_state.document
    ).replace(
        "\n",
        "<br>"
    )

    st.markdown(
        f"""
<div class="preview">
{preview_text}
</div>
""",
        unsafe_allow_html=True
    )

    # -------------------------
    # Editor
    # -------------------------

    st.subheader(
        "✏️ Edit Document"
    )

    edited = st.text_area(
        "Edit the generated document "
        "before exporting.",
        value=st.session_state.document,
        height=500,
        label_visibility="collapsed"
    )

    st.session_state.document = edited

    # -------------------------
    # Downloads
    # -------------------------

    st.subheader(
        "⬇️ Download"
    )

    col1, col2, col3 = st.columns(
        3
    )

    safe_name = "".join(
        character
        if character.isalnum()
        or character in "-_"
        else "_"
        for character
        in st.session_state.generated_type
    ).strip("_")

    if not safe_name:

        safe_name = "legal_document"


    # TXT
    with col1:

        txt_data = format_txt(
            st.session_state.document
        )

        st.download_button(
            "⬇️ Download TXT",
            data=txt_data,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True
        )


    # DOCX
    with col2:

        docx_data = format_docx(
            st.session_state.document,
            st.session_state.generated_type,
            terms
        )

        st.download_button(
            "⬇️ Download DOCX",
            data=docx_data,
            file_name=f"{safe_name}.docx",
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True
        )


    # PDF
    with col3:

        pdf_data = format_pdf(
            st.session_state.document,
            st.session_state.generated_type
        )

        st.download_button(
            "⬇️ Download PDF",
            data=pdf_data,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

else:

    st.caption(
        "Your generated document will appear here."
    )