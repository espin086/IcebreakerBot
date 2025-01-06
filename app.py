import streamlit as st
from icebreaker.icebreaker import icebreaker


# Streamlit app
def main():
    st.title("LinkedIn Icebreaker Generator")

    # Input from user
    name = st.text_input("Enter name of person to find on Linkedin")

    # Generate icebreaker when the button is clicked
    if st.button("Generate Icebreaker"):
        if name:
            # Call the icebreaker function and display the result
            try:
                result = icebreaker(name)
                st.write(result)
            except Exception as e:
                st.error(f"Error occurred: {e}")
        else:
            st.warning("Please enter a LinkedIn username.")


if __name__ == "__main__":
    main()
