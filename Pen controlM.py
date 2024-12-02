



   # logical order : is button pressed ? change the state if up turn light on, if down turn the light off, wait 3sec then start again
    # Set up button and light for pen control
button = Pin(15, Pin.IN, Pin.PULL_DOWN)  # Bouton connecté à GPIO 15
light = Pin(2, Pin.OUT)  # Lumière connectée à GPIO 2

# Pen control function
def pen_control():
    try:
        if button.value():  # Vérifie si le bouton est pressé
            light.value(1)  # Allume la lumière
            print("Pen is up, light ON")
        else:
            light.value(0)  # Éteint la lumière
            print("Pen is down, light OFF")
        time.sleep(0.3)  # Pause de 0.3 seconde avant de recommencer
    except Exception as e:
        print(f"Error in pen control: {e}")
    
# Call pen control in the main loop
while True:
    pen_control()

#emergency handling
#use a while true fonction that we will return the element to the intial state 0 with a print statement
# Configuration du bouton d'urgence et des éléments à contrôler
emergency_button = Pin(14, Pin.IN, Pin.PULL_DOWN)  # Bouton d'urgence connecté à GPIO 14
light = Pin(2, Pin.OUT)  # Lumière déjà configurée pour le pen control

def emergency_handling():
     if emergency_button.value():  # Si le bouton d'urgence est pressé
         light.value(0)  # Éteint la lumière ou tout autre dispositif
         print("Emergency triggered! All elements reset to initial state.")
        time.sleep(0.3)  # Pause pour éviter une répétition rapide du message
    else:
            time.sleep(0.3)  # Vérifie à nouveau l'état du bouton après un court délai

# Appel de la gestion d'urgence
emergency_handling()

