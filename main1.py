import socket
import threading
import tkinter as tk
from tkinter import colorchooser, messagebox
import secrets


# ============================================================
# DIFFIE-HELLMAN PUBLIC PARAMETERS
# ============================================================

# 2048-bit MODP prime commonly used for DH demonstrations.
# Generator = 2
#
# IMPORTANT:
# The paint/color portion of this program is only a VISUAL
# REPRESENTATION. The actual shared secret is calculated using
# Diffie-Hellman mathematics.

DH_PRIME = int(
    """
    FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1
    29024E088A67CC74020BBEA63B139B22514A08798E3404DD
    EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245
    E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED
    EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC
    2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83
    65D1B3A1D7D7B0B0
    """.replace("\n", "").replace(" ", ""),
    16
)

DH_GENERATOR = 2

PORT = 12345


# ============================================================
# PAINT / COLOR FUNCTIONS
# ============================================================

# Public color that everyone knows.
PUBLIC_BASE_COLOR = (100, 100, 100)


def mix_paint(color1, color2):
    """
    Simple RGB averaging used ONLY for visualization.
    This is NOT the cryptographic operation.
    """

    r = (color1[0] + color2[0]) // 2
    g = (color1[1] + color2[1]) // 2
    b = (color1[2] + color2[2]) // 2

    return r, g, b


def rgb_to_hex(rgb):
    """
    Convert RGB tuple to hexadecimal color.
    """

    return "#{:02x}{:02x}{:02x}".format(
        rgb[0],
        rgb[1],
        rgb[2]
    )


def secret_to_color(shared_secret):
    """
    Convert the Diffie-Hellman shared secret into an RGB color.

    This is ONLY for visualization.

    The actual cryptographic shared secret remains the large
    integer produced by Diffie-Hellman.
    """

    r = shared_secret & 0xFF

    g = (shared_secret >> 8) & 0xFF

    b = (shared_secret >> 16) & 0xFF

    return r, g, b


# ============================================================
# MAIN APPLICATION
# ============================================================

class DiffieHellmanPaintApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Diffie-Hellman Paint Exchange"
        )

        self.root.geometry(
            "700x750"
        )

        self.root.minsize(
            550,
            500
        )

        # ====================================================
        # NETWORK VARIABLES
        # ====================================================

        self.conn = None

        self.server_socket = None

        # ====================================================
        # DIFFIE-HELLMAN VARIABLES
        # ====================================================

        self.private_key = None

        self.public_key = None

        self.other_public_key = None

        self.shared_secret = None

        # ====================================================
        # PAINT VARIABLES
        # ====================================================

        self.secret_color = (0, 0, 0)

        self.my_mix = None

        self.shared_color = None

        # ====================================================
        # CREATE SCROLLABLE UI
        # ====================================================

        self.create_scrollable_interface()

        self.create_widgets()

        # Handle window closing
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )


    # ========================================================
    # SCROLLABLE INTERFACE
    # ========================================================

    def create_scrollable_interface(self):

        # Main canvas

        self.canvas = tk.Canvas(
            self.root,
            highlightthickness=0
        )

        self.canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )


        # Scrollbar

        self.scrollbar = tk.Scrollbar(
            self.root,
            orient=tk.VERTICAL,
            command=self.canvas.yview
        )

        self.scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )


        # Frame inside canvas

        self.scrollable_frame = tk.Frame(
            self.canvas
        )


        self.canvas_window = (
            self.canvas.create_window(
                (0, 0),
                window=self.scrollable_frame,
                anchor="nw"
            )
        )


        # Update scroll region when frame changes

        self.scrollable_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )


        # Make inner frame width match canvas

        self.canvas.bind(
            "<Configure>",
            self.resize_scrollable_frame
        )


        # Mouse wheel

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )


    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )


    def resize_scrollable_frame(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )


    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    # ========================================================
    # UI CREATION
    # ========================================================

    def create_widgets(self):

        frame = self.scrollable_frame


        # ====================================================
        # TITLE
        # ====================================================

        tk.Label(
            frame,
            text="🔐 Diffie-Hellman Paint Exchange",
            font=("Arial", 20, "bold")
        ).pack(
            pady=(20, 5)
        )


        tk.Label(
            frame,
            text=(
                "Real Diffie-Hellman mathematics "
                "+ visual paint mixing"
            ),
            font=("Arial", 10)
        ).pack(
            pady=(0, 15)
        )


        # ====================================================
        # STEP 1 - NETWORK
        # ====================================================

        self.create_section_title(
            frame,
            "1. Network Setup"
        )


        ip_frame = tk.Frame(frame)

        ip_frame.pack(
            pady=5
        )


        tk.Label(
            ip_frame,
            text="Server IP:",
            font=("Arial", 10)
        ).pack(
            side=tk.LEFT
        )


        self.ip_entry = tk.Entry(
            ip_frame,
            width=20
        )

        self.ip_entry.insert(
            0,
            "127.0.0.1"
        )

        self.ip_entry.pack(
            side=tk.LEFT,
            padx=8
        )


        button_frame = tk.Frame(frame)

        button_frame.pack(
            pady=8
        )


        tk.Button(
            button_frame,
            text="Start as Server",
            command=self.start_server,
            bg="#4CAF50",
            fg="white",
            width=16
        ).pack(
            side=tk.LEFT,
            padx=5
        )


        tk.Button(
            button_frame,
            text="Connect to Server",
            command=self.start_client,
            bg="#2196F3",
            fg="white",
            width=16
        ).pack(
            side=tk.LEFT,
            padx=5
        )


        self.status_label = tk.Label(
            frame,
            text="Status: Not Connected",
            fg="red",
            font=("Arial", 10, "bold")
        )

        self.status_label.pack(
            pady=8
        )


        # ====================================================
        # STEP 2 - PUBLIC PARAMETERS
        # ====================================================

        self.create_section_title(
            frame,
            "2. Public Diffie-Hellman Parameters"
        )


        parameter_frame = tk.Frame(frame)

        parameter_frame.pack(
            pady=5
        )


        tk.Label(
            parameter_frame,
            text="Generator (g):",
            font=("Arial", 10, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=3
        )


        tk.Label(
            parameter_frame,
            text=str(DH_GENERATOR)
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=5
        )


        tk.Label(
            parameter_frame,
            text="Prime (p):",
            font=("Arial", 10, "bold")
        ).grid(
            row=1,
            column=0,
            sticky="nw",
            padx=5,
            pady=3
        )


        prime_display = (
            hex(DH_PRIME)[:50]
            + "..."
        )


        tk.Label(
            parameter_frame,
            text=prime_display,
            wraplength=500,
            justify="left"
        ).grid(
            row=1,
            column=1,
            sticky="w",
            padx=5
        )


        # ====================================================
        # PUBLIC BASE PAINT
        # ====================================================

        tk.Label(
            frame,
            text="Public Base Paint",
            font=("Arial", 11, "bold")
        ).pack(
            pady=(15, 3)
        )


        self.base_patch = tk.Label(
            frame,
            text=rgb_to_hex(
                PUBLIC_BASE_COLOR
            ).upper(),
            width=30,
            height=2,
            bg=rgb_to_hex(
                PUBLIC_BASE_COLOR
            ),
            relief="solid"
        )

        self.base_patch.pack(
            pady=5
        )


        # ====================================================
        # STEP 3 - PRIVATE PAINT
        # ====================================================

        self.create_section_title(
            frame,
            "3. Choose Your Private Paint"
        )


        self.btn_secret = tk.Button(
            frame,
            text="Pick Secret Color",
            command=self.choose_secret,
            state=tk.DISABLED,
            width=25
        )

        self.btn_secret.pack(
            pady=5
        )


        self.secret_patch = tk.Label(
            frame,
            text="No Private Paint Chosen",
            width=30,
            height=2,
            bg="white",
            relief="solid"
        )

        self.secret_patch.pack(
            pady=5
        )


        # ====================================================
        # STEP 4 - GENERATE PUBLIC KEY
        # ====================================================

        self.create_section_title(
            frame,
            "4. Generate Your DH Public Key"
        )


        self.btn_generate = tk.Button(
            frame,
            text="Generate Public Key",
            command=self.generate_keys,
            state=tk.DISABLED,
            width=25
        )

        self.btn_generate.pack(
            pady=5
        )


        self.public_key_label = tk.Label(
            frame,
            text="Your Public Key: Not Generated",
            wraplength=600,
            justify="left"
        )

        self.public_key_label.pack(
            pady=5
        )


        # ====================================================
        # STEP 5 - SEND PUBLIC KEY
        # ====================================================

        self.create_section_title(
            frame,
            "5. Exchange Public Keys"
        )


        self.btn_send = tk.Button(
            frame,
            text="Send Public Key",
            command=self.send_public_key,
            state=tk.DISABLED,
            width=25
        )

        self.btn_send.pack(
            pady=5
        )


        self.received_key_label = tk.Label(
            frame,
            text="Friend's Public Key: Waiting...",
            wraplength=600,
            justify="left"
        )

        self.received_key_label.pack(
            pady=5
        )


        # ====================================================
        # STEP 6 - SHARED SECRET
        # ====================================================

        self.create_section_title(
            frame,
            "6. Generate Shared Secret"
        )


        self.btn_shared = tk.Button(
            frame,
            text="Calculate Shared Secret",
            command=self.calculate_shared_secret,
            state=tk.DISABLED,
            width=25,
            bg="#FF9800",
            fg="white"
        )

        self.btn_shared.pack(
            pady=8
        )


        self.shared_label = tk.Label(
            frame,
            text="Shared Secret: Waiting...",
            wraplength=600,
            justify="left"
        )

        self.shared_label.pack(
            pady=5
        )


        # ====================================================
        # STEP 7 - FINAL PAINT
        # ====================================================

        self.create_section_title(
            frame,
            "7. Shared Secret Paint"
        )


        self.final_patch = tk.Label(
            frame,
            text=(
                "Waiting for Diffie-Hellman exchange..."
            ),
            width=40,
            height=5,
            bg="white",
            relief="solid",
            font=("Arial", 12, "bold")
        )

        self.final_patch.pack(
            pady=10
        )


        # ====================================================
        # EXPLANATION
        # ====================================================

        explanation = (
            "How it works:\n\n"
            "1. Both computers know public values g and p.\n"
            "2. Each computer generates a private key.\n"
            "3. Each computer calculates a public key.\n"
            "4. Public keys are exchanged over TCP.\n"
            "5. Each computer calculates the same shared secret.\n"
            "6. The shared secret is converted into a color.\n\n"
            "The paint is a visual representation only.\n"
            "The actual secret comes from Diffie-Hellman mathematics."
        )


        tk.Label(
            frame,
            text=explanation,
            justify="left",
            wraplength=600,
            font=("Arial", 10)
        ).pack(
            pady=(10, 30)
        )


    # ========================================================
    # SECTION TITLE HELPER
    # ========================================================

    def create_section_title(
        self,
        frame,
        title
    ):

        tk.Label(
            frame,
            text=title,
            font=("Arial", 13, "bold")
        ).pack(
            pady=(18, 8)
        )


    # ========================================================
    # SERVER
    # ========================================================

    def start_server(self):

        self.status_label.config(
            text=(
                "Server starting...\n"
                "Waiting for another laptop..."
            ),
            fg="orange"
        )


        def server_thread():

            try:

                self.server_socket = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )


                self.server_socket.setsockopt(
                    socket.SOL_SOCKET,
                    socket.SO_REUSEADDR,
                    1
                )


                self.server_socket.bind(
                    (
                        "0.0.0.0",
                        PORT
                    )
                )


                self.server_socket.listen(1)


                # Determine local IP

                try:

                    hostname = socket.gethostname()

                    local_ip = socket.gethostbyname(
                        hostname
                    )

                except:

                    local_ip = "Unknown"


                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text=(
                            f"Server running!\n"
                            f"Your IP: {local_ip}\n"
                            f"Port: {PORT}\n"
                            f"Waiting for friend..."
                        ),
                        fg="orange"
                    )
                )


                # Wait for client

                self.conn, address = (
                    self.server_socket.accept()
                )


                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text=(
                            f"Connected!\n"
                            f"Friend: {address[0]}"
                        ),
                        fg="green"
                    )
                )


                # Enable secret color selection

                self.root.after(
                    0,
                    lambda: self.btn_secret.config(
                        state=tk.NORMAL
                    )
                )


                # Start receiving thread

                threading.Thread(
                    target=self.receive_messages,
                    daemon=True
                ).start()


            except Exception as e:

                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Server Error",
                        str(e)
                    )
                )


        threading.Thread(
            target=server_thread,
            daemon=True
        ).start()


    # ========================================================
    # CLIENT
    # ========================================================

    def start_client(self):

        target_ip = (
            self.ip_entry
            .get()
            .strip()
        )


        if not target_ip:

            messagebox.showwarning(
                "Missing IP",
                "Enter the server IP address."
            )

            return


        self.status_label.config(
            text="Connecting...",
            fg="orange"
        )


        def client_thread():

            try:

                self.conn = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )


                self.conn.settimeout(10)


                self.conn.connect(
                    (
                        target_ip,
                        PORT
                    )
                )


                self.conn.settimeout(None)


                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text=(
                            f"Connected to server!\n"
                            f"{target_ip}:{PORT}"
                        ),
                        fg="green"
                    )
                )


                self.root.after(
                    0,
                    lambda: self.btn_secret.config(
                        state=tk.NORMAL
                    )
                )


                threading.Thread(
                    target=self.receive_messages,
                    daemon=True
                ).start()


            except Exception as e:

                self.root.after(
                    0,
                    lambda: messagebox.showerror(
                        "Connection Error",
                        (
                            f"Could not connect to "
                            f"{target_ip}:{PORT}\n\n"
                            f"{e}"
                        )
                    )
                )


                self.root.after(
                    0,
                    lambda: self.status_label.config(
                        text="Connection Failed",
                        fg="red"
                    )
                )


        threading.Thread(
            target=client_thread,
            daemon=True
        ).start()


    # ========================================================
    # RECEIVE DATA
    # ========================================================

    def receive_messages(self):

        buffer = ""


        try:

            while True:

                data = self.conn.recv(4096)


                if not data:

                    break


                buffer += data.decode()


                # Messages end with newline

                while "\n" in buffer:

                    message, buffer = (
                        buffer.split(
                            "\n",
                            1
                        )
                    )


                    message = message.strip()


                    if not message:

                        continue


                    # ----------------------------------------
                    # PUBLIC KEY
                    # ----------------------------------------

                    if message.startswith(
                        "PUBLIC_KEY:"
                    ):

                        key_string = (
                            message.split(
                                ":",
                                1
                            )[1]
                        )


                        received_key = int(
                            key_string
                        )


                        self.other_public_key = (
                            received_key
                        )


                        self.root.after(
                            0,
                            lambda k=received_key:
                            self.display_received_key(k)
                        )


        except Exception as e:

            print(
                "Receive error:",
                e
            )


    # ========================================================
    # DISPLAY RECEIVED KEY
    # ========================================================

    def display_received_key(
        self,
        key
    ):

        key_text = str(key)


        if len(key_text) > 55:

            key_text = (
                key_text[:55]
                + "..."
            )


        self.received_key_label.config(
            text=(
                "Friend's Public Key:\n"
                + key_text
            ),
            fg="green"
        )


        # If our public key exists, allow calculation

        if self.public_key is not None:

            self.btn_shared.config(
                state=tk.NORMAL
            )


    # ========================================================
    # CHOOSE PRIVATE PAINT
    # ========================================================

    def choose_secret(self):

        color_code = colorchooser.askcolor(
            title="Choose Your Private Paint"
        )


        if color_code[0] is None:

            return


        self.secret_color = tuple(
            map(
                int,
                color_code[0]
            )
        )


        self.secret_patch.config(
            bg=color_code[1],
            text=(
                "Private Paint: "
                + color_code[1].upper()
            )
        )


        self.btn_generate.config(
            state=tk.NORMAL
        )


    # ========================================================
    # GENERATE DH KEYS
    # ========================================================

    def generate_keys(self):

        # ----------------------------------------------------
        # Generate random private key
        #
        # a = random number
        # ----------------------------------------------------

        self.private_key = (
            secrets.randbelow(
                DH_PRIME - 2
            ) + 2
        )


        # ----------------------------------------------------
        # Calculate public key
        #
        # A = g^a mod p
        # ----------------------------------------------------

        self.public_key = pow(
            DH_GENERATOR,
            self.private_key,
            DH_PRIME
        )


        public_key_text = str(
            self.public_key
        )


        if len(public_key_text) > 60:

            display_key = (
                public_key_text[:60]
                + "..."
            )

        else:

            display_key = public_key_text


        self.public_key_label.config(
            text=(
                "Your Public Key:\n"
                + display_key
            ),
            fg="green"
        )


        self.btn_send.config(
            state=tk.NORMAL
        )


        # If friend's key already arrived

        if self.other_public_key is not None:

            self.btn_shared.config(
                state=tk.NORMAL
            )


    # ========================================================
    # SEND PUBLIC KEY
    # ========================================================

    def send_public_key(self):

        if self.conn is None:

            messagebox.showwarning(
                "Not Connected",
                "Connect to another laptop first."
            )

            return


        if self.public_key is None:

            messagebox.showwarning(
                "No Public Key",
                "Generate your public key first."
            )

            return


        message = (
            f"PUBLIC_KEY:{self.public_key}\n"
        )


        try:

            self.conn.sendall(
                message.encode()
            )


            self.btn_send.config(
                state=tk.DISABLED
            )


            self.public_key_label.config(
                text=(
                    self.public_key_label.cget(
                        "text"
                    )
                    + "\n✓ Public key sent!"
                )
            )


            # If we already received friend's key

            if self.other_public_key is not None:

                self.btn_shared.config(
                    state=tk.NORMAL
                )


        except Exception as e:

            messagebox.showerror(
                "Network Error",
                str(e)
            )


    # ========================================================
    # CALCULATE SHARED SECRET
    # ========================================================

    def calculate_shared_secret(self):

        if self.private_key is None:

            messagebox.showwarning(
                "Missing Private Key",
                "Generate your public key first."
            )

            return


        if self.other_public_key is None:

            messagebox.showwarning(
                "Waiting",
                "Waiting for your friend's public key."
            )

            return


        # ====================================================
        # REAL DIFFIE-HELLMAN
        #
        # Suppose we are Alice:
        #
        # private = a
        # friend's public key = B
        #
        # Shared secret:
        #
        # K = B^a mod p
        #
        # Friend calculates:
        #
        # K = A^b mod p
        #
        # Both are equal to:
        #
        # K = g^(ab) mod p
        # ====================================================

        self.shared_secret = pow(
            self.other_public_key,
            self.private_key,
            DH_PRIME
        )


        # ----------------------------------------------------
        # Display shared secret
        # ----------------------------------------------------

        secret_text = str(
            self.shared_secret
        )


        if len(secret_text) > 70:

            display_secret = (
                secret_text[:70]
                + "..."
            )

        else:

            display_secret = secret_text


        self.shared_label.config(
            text=(
                "✓ Shared Secret Generated!\n"
                + display_secret
            ),
            fg="green"
        )


        # ----------------------------------------------------
        # Convert shared secret to color
        # ----------------------------------------------------

        self.shared_color = secret_to_color(
            self.shared_secret
        )


        hex_color = rgb_to_hex(
            self.shared_color
        )


        # ----------------------------------------------------
        # Display final color
        # ----------------------------------------------------

        self.final_patch.config(
            bg=hex_color,
            text=(
                "🔐 SHARED SECRET PAINT\n\n"
                + hex_color.upper()
            ),
            fg="black"
        )


        # ----------------------------------------------------
        # Show detailed explanation
        # ----------------------------------------------------

        self.show_dh_result()


    # ========================================================
    # SHOW DH RESULT
    # ========================================================

    def show_dh_result(self):

        window = tk.Toplevel(
            self.root
        )


        window.title(
            "Diffie-Hellman Result"
        )


        window.geometry(
            "600x650"
        )


        # Scrollable popup

        canvas = tk.Canvas(
            window
        )

        scrollbar = tk.Scrollbar(
            window,
            orient="vertical",
            command=canvas.yview
        )


        content = tk.Frame(
            canvas
        )


        content.bind(
            "<Configure>",
            lambda e:
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )


        canvas.create_window(
            (0, 0),
            window=content,
            anchor="nw"
        )


        canvas.configure(
            yscrollcommand=scrollbar.set
        )


        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )


        scrollbar.pack(
            side="right",
            fill="y"
        )


        # ====================================================
        # TITLE
        # ====================================================

        tk.Label(
            content,
            text="🔐 Diffie-Hellman Complete",
            font=("Arial", 18, "bold")
        ).pack(
            pady=20
        )


        # ====================================================
        # PRIVATE KEY
        # ====================================================

        tk.Label(
            content,
            text="Your Private Key",
            font=("Arial", 12, "bold")
        ).pack()


        tk.Label(
            content,
            text=str(
                self.private_key
            )[:80],
            wraplength=550
        ).pack(
            pady=5
        )


        # ====================================================
        # PUBLIC KEY
        # ====================================================

        tk.Label(
            content,
            text="Your Public Key",
            font=("Arial", 12, "bold")
        ).pack(
            pady=(15, 0)
        )


        tk.Label(
            content,
            text=str(
                self.public_key
            )[:80],
            wraplength=550
        ).pack(
            pady=5
        )


        # ====================================================
        # FRIEND PUBLIC KEY
        # ====================================================

        tk.Label(
            content,
            text="Friend's Public Key",
            font=("Arial", 12, "bold")
        ).pack(
            pady=(15, 0)
        )


        tk.Label(
            content,
            text=str(
                self.other_public_key
            )[:80],
            wraplength=550
        ).pack(
            pady=5
        )


        # ====================================================
        # SHARED SECRET
        # ====================================================

        tk.Label(
            content,
            text="Shared Secret",
            font=("Arial", 12, "bold")
        ).pack(
            pady=(15, 0)
        )


        tk.Label(
            content,
            text=str(
                self.shared_secret
            )[:100],
            wraplength=550,
            fg="green"
        ).pack(
            pady=5
        )


        # ====================================================
        # FINAL PAINT
        # ====================================================

        tk.Label(
            content,
            text="Final Shared Secret Paint",
            font=("Arial", 12, "bold")
        ).pack(
            pady=(20, 5)
        )


        color = rgb_to_hex(
            self.shared_color
        )


        tk.Label(
            content,
            width=35,
            height=5,
            bg=color,
            text=color.upper(),
            relief="solid",
            font=("Arial", 14, "bold")
        ).pack(
            pady=10
        )


        # ====================================================
        # MATHEMATICAL EXPLANATION
        # ====================================================

        explanation = (
            "Diffie-Hellman calculation:\n\n"
            "Public parameters:\n"
            "    g = generator\n"
            "    p = large prime\n\n"
            "Your private key:\n"
            "    a\n\n"
            "Your public key:\n"
            "    A = g^a mod p\n\n"
            "Friend's public key:\n"
            "    B = g^b mod p\n\n"
            "Your shared secret:\n"
            "    K = B^a mod p\n\n"
            "Friend's shared secret:\n"
            "    K = A^b mod p\n\n"
            "Therefore:\n"
            "    B^a mod p = A^b mod p\n\n"
            "Both computers obtain the SAME shared secret.\n\n"
            "The RGB color is generated from that shared secret\n"
            "only as a visual representation."
        )


        tk.Label(
            content,
            text=explanation,
            justify="left",
            wraplength=550,
            font=("Arial", 10)
        ).pack(
            pady=20
        )


    # ========================================================
    # CLOSE APPLICATION
    # ========================================================

    def close_application(self):

        try:

            if self.conn:

                self.conn.close()

        except:

            pass


        try:

            if self.server_socket:

                self.server_socket.close()

        except:

            pass


        self.root.destroy()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = DiffieHellmanPaintApp(
        root
    )

    root.mainloop()