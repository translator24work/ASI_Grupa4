import streamlit as st
from kedro.framework.context import load_context

# Load Kedro context
kedro_context = load_context('/kedro-asi/')


# Define your Streamlit app
def main():
    st.title("My Kedro-Streamlit Integration")

    if st.button("Run Kedro Pipeline"):
        # This will run the entire pipeline
        kedro_context.run()

        # Optional: Display a message upon completion
        st.success("Kedro pipeline executed successfully!")


# Run the Streamlit app
if __name__ == "__main__":
    main()
