import bpy

# Addon information (essential for proper addon setup)
bl_info = {
    "name": "Simple Pop-up Input with Cancel Handling",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Anywhere (triggered by script)",
    "description": "A simple pop-up to get string input from the user, with custom cancel handling.",
    "category": "Development",
}

# 1. Define the Pop-up Operator
class MY_OT_SimpleStringPopup(bpy.types.Operator):
    """Simple operator to get a string input via a pop-up dialog"""
    bl_idname = "myaddon.simple_string_popup" # Unique ID for the operator (lowercase, no spaces)
    bl_label = "Enter Text"                   # Title of the pop-up window
    bl_options = {'REGISTER'}                 # 'REGISTER' is crucial for invoke_props_dialog

    # Property to be displayed in the pop-up for user input
    user_input_text: bpy.props.StringProperty(
        name="Your Text",
        description="Please enter some text here",
        default="Default text..."
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Please type your message below:")
        layout.prop(self, "user_input_text") # Display the string property

    def execute(self, context):
        entered_text = self.user_input_text
        self.report({'INFO'}, f"User entered: '{entered_text}'")
        print(f"\n--- Pop-up Result (Executed) ---")
        print(f"User entered: '{entered_text}'")
        print(f"--------------------------------\n")
        return {'FINISHED'}

    # This method runs if the user clicks 'Cancel', presses Esc, or clicks outside the dialog.
    def cancel(self, context):
        # --- This is where you "handle the error" of cancellation ---
        custom_error_message = "Input was cancelled by user (clicked outside or pressed ESC)."
        
        # 1. Report an ERROR message to the user (appears in the info bar at the top)
        self.report({'ERROR'}, custom_error_message)
        
        # 2. Print a detailed message to the console for debugging
        print(f"\n--- Pop-up Result (Cancelled) ---")
        print(f"ERROR: {custom_error_message}")
        print(f"No text was processed. Current value: '{self.user_input_text}'")
        print(f"-----------------------------------\n")
        
        # 3. (Optional) You could raise a Python exception here for very specific debugging,
        #    but it's generally NOT recommended for production addons as it creates tracebacks
        #    for normal user behavior.
        # raise ValueError("Operation cancelled by user!")

        return {'CANCELLED'} # This tells Blender the operator was cancelled


# 2. Registration and Unregistration functions
classes = (
    MY_OT_SimpleStringPopup,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("Simple Pop-up Input Addon Registered!")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    print("Simple Pop-up Input Addon Unregistered!")

# This makes the script runnable directly from Blender's Text Editor for testing.
if __name__ == "__main__":
    register()
    # To test, uncomment the line below and run the script.
    # bpy.ops.myaddon.simple_string_popup('INVOKE_DEFAULT')