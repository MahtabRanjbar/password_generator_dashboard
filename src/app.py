import streamlit as st
from nltk.corpus import words

from password_generator import (RandomPasswordGenerator,
                                MemorablePasswordGenerator,
                                PinCodeGenerator,
                                check_password_strength)


def main():
    st.set_page_config(page_title="Advanced Password Generator", page_icon="🔐", layout="wide")

    # Custom CSS to control the banner size
    st.markdown("""
        <style>
        .banner-img {
            width: 20%;
            max-height: 50px;
            object-fit: cover;
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
        </style>
        """, unsafe_allow_html=True)

    # Banner and Title
    st.markdown('<div class="banner-img">', unsafe_allow_html=True)
    st.image('./images/banner.jpeg', use_column_width=False)
    st.markdown('</div>', unsafe_allow_html=True)
    st.title("🔐 Advanced Password Generator")

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Generate Password")
        option = st.radio("Password Type", ('Random Password', 'Memorable Password', 'Pin Code'))

        if option == 'Random Password':
            length = st.slider("Length", min_value=5, max_value=50, value=12)
            include_numbers = st.checkbox("Include Numbers", value=True)
            include_symbols = st.checkbox("Include Symbols", value=True)
            generator = RandomPasswordGenerator(length, include_numbers,
                                                include_symbols)

        elif option == 'Memorable Password':
            no_of_words = st.slider("Number of Words",
                                    min_value=2,
                                    max_value=10,
                                    value=4)
            separator = st.text_input("Separator", value='-')
            capitalization = st.checkbox("Capitalize Words", value=True)
            generator = MemorablePasswordGenerator(no_of_words, separator,
                                                   capitalization, words.words())

        else:
            length = st.slider("Length", min_value=2, max_value=10, value=4)
            generator = PinCodeGenerator(length)

        if st.button("Generate Password", key="generate"):
            password = generator.generate()
            st.session_state.password = password
            st.session_state.password_strength = check_password_strength(password)

        if 'password' in st.session_state:
            st.subheader("Generated Password:")
            st.code(st.session_state.password, language="")
            st.write(f"Password Strength: {st.session_state.password_strength}")

            # Copy to clipboard button
            st.markdown(
                f"""
                <button onclick="navigator.clipboard.writeText('{st.session_state.password}')">
                    Copy to Clipboard
                </button>
                """,
                unsafe_allow_html=True
            )

    with col2:
        # Password History
        if 'password_history' not in st.session_state:
            st.session_state.password_history = []

        if 'password' in st.session_state and st.session_state.password not in st.session_state.password_history:
            st.session_state.password_history.append(st.session_state.password)

        if st.session_state.password_history:
            st.subheader("Password History")
            for idx, hist_password in enumerate(reversed(st.session_state.password_history[-5:]), 1):
                st.text(f"{idx}. {hist_password}")

    # Sidebar
    with st.sidebar:
        st.header("Additional Features")

        # Password Strength Checker
        st.subheader("Password Strength Checker")
        custom_password = st.text_input("Enter a password to check its strength:", type="password")
        if custom_password:
            strength = check_password_strength(custom_password)
            st.write(f"Password Strength: {strength}")

        # Expandable sections for additional information
        with st.expander("Password Policy"):
            st.write("""
            For a strong password:
            - Use at least 12 characters
            - Include a mix of uppercase and lowercase letters
            - Include numbers and symbols
            - Avoid common words or phrases
            """)

        with st.expander("Additional Information"):
            st.write("""
            This advanced password generator provides three types of passwords:
            1. **Random Password**: A combination of letters, numbers, and symbols.
            2. **Memorable Password**: A series of random words, easier to remember.
            3. **Pin Code**: A sequence of random digits.

            Always use unique passwords for different accounts and consider using a password manager for added security.
            """)


if __name__ == "__main__":
    main()
