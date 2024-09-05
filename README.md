# Overview
The Murchison Widefield Array (MWA) is the largest ground-based Radio Telescope built to create exquisite real-time wide-field images of the undiscovered low frequency radio-phenomena of the radio sky. A state of the art Digital Receiver was built to provide configurable modes and features to aid observation through remote operation controlled by complex C programs. wMARC (web-based Murchison Widefield Array Receiver Console) is a
sub-project for the MWA, and is developed specifically to facilitate a nice interface for the receiver experts, which hides the internal operations but provides the needed real-time control and status monitoring from anywhere in the world.

# Instructions to launch the application
1. Launch unix terminal window
2. Change directory to .../www
3. Run Python local cgi server by giving the following command: python -m CGIHTTPServer
4. Launch URL address: http://<yourhostname>/cgi-bin/main_program.cgi (For example, 'yourhostname' can be 'localhost:8000')
5. Start your testing session.
