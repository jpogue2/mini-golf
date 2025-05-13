const int buttonPins[] = {2, 3, 4, 5};  // Button pins array
const String messages[] = {"042", "019", "027", "001"};  // Corresponding messages
int lastButtonStates[] = {HIGH, HIGH, HIGH, HIGH};  // Previous states for each button
unsigned long lastPressTimes[] = {0, 0, 0, 0};  // Last press timestamps
const int debounceDelay = 250;  // Debounce delay in milliseconds

void setup() {
    for (int i = 0; i < 4; i++) {
        pinMode(buttonPins[i], INPUT_PULLUP);  // Enable internal pull-up resistors
    }
    Serial.begin(9600);  // Initialize serial communication
}

void loop() {
    unsigned long currentTime = millis();  // Get the current time

    for (int i = 0; i < 4; i++) {
        int buttonState = digitalRead(buttonPins[i]);  // Read the current state of the button

        // Detect a button press (transition from HIGH to LOW) and check debounce time
        if (buttonState == LOW && lastButtonStates[i] == HIGH && (currentTime - lastPressTimes[i] > debounceDelay)) {
            Serial.println(messages[i]);  // Send the corresponding message
            lastPressTimes[i] = currentTime;  // Update last press time
        }

        lastButtonStates[i] = buttonState;  // Update the last state of the button
    }
}
