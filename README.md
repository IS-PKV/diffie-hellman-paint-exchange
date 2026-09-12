# 🔐 Diffie-Hellman Paint Exchange

A **Python-based secure key exchange demonstration** that implements the **Diffie-Hellman Key Exchange algorithm** over a TCP network and visualizes the resulting shared secret as a color.

The project combines **cryptography, socket programming, multithreading, and Tkinter GUI development** to demonstrate how two devices can establish the same secret without directly transmitting the secret itself.

> 🎨 **The paint/color is only a visualization. The actual shared secret is generated using Diffie-Hellman mathematics.**

---

## ✨ Features

* 🔐 Real Diffie-Hellman key exchange
* 🌐 TCP socket communication between two computers
* 🖥️ Interactive Tkinter GUI
* 🔑 Random private key generation using Python's `secrets` module
* 📡 Public-key exchange over a network
* 🎨 Converts the resulting shared secret into an RGB color
* 📜 Displays the Diffie-Hellman mathematical process
* 🔄 Scrollable interface for the complete workflow
* 🧵 Background threads for network communication
* ✅ Visual verification that both devices generated the same shared secret

---

## 🧠 Project Concept

The project demonstrates the basic idea behind **Diffie-Hellman Key Exchange**.

Two users, Alice and Bob, want to establish a shared secret.

They publicly agree on:

* A large prime number `p`
* A generator `g`

Each user then generates their own private key.

### Alice

Alice chooses a private key:

```text
a
```

and calculates:

```text
A = g^a mod p
```

### Bob

Bob chooses a private key:

```text
b
```

and calculates:

```text
B = g^b mod p
```

Alice and Bob exchange only their **public keys**.

Alice calculates:

```text
K = B^a mod p
```

Bob calculates:

```text
K = A^b mod p
```

Both values are mathematically equal:

```text
B^a mod p = A^b mod p
```

Therefore:

```text
                 SAME SHARED SECRET
                         🔐
                    K = g^(ab) mod p
```

The private keys `a` and `b` are never transmitted.

---

## 🎨 Paint Visualization

To make the cryptographic process easier to understand visually, the shared secret is converted into an RGB color.

The generated DH shared secret is a very large integer.

The program extracts three bytes from the integer:

```python
r = shared_secret & 0xFF
g = (shared_secret >> 8) & 0xFF
b = (shared_secret >> 16) & 0xFF
```

These values are converted into:

```text
RGB → Hexadecimal Color
```

For example:

```text
Shared Secret
      ↓
Large Integer
      ↓
 ┌────┬────┬────┐
 │ R  │ G  │ B  │
 └────┴────┴────┘
      ↓
   #A4C281
      ↓
🎨 Shared Secret Paint
```

If both computers correctly perform the Diffie-Hellman exchange, they generate the **same shared secret and therefore the same color**.

---

## 🌐 Network Architecture

The application uses a simple TCP client-server architecture.

```text
                 TCP CONNECTION
        ┌───────────────────────────┐
        │                           │
        ▼                           ▼
┌───────────────┐             ┌───────────────┐
│   Laptop 1    │             │   Laptop 2    │
│               │             │               │
│    SERVER     │◄───────────►│    CLIENT     │
│               │             │               │
│ Private Key   │             │ Private Key   │
│ Public Key    │             │ Public Key    │
└───────────────┘             └───────────────┘
        │                           │
        │       Public Keys         │
        └───────────┬───────────────┘
                    │
                    ▼
             Shared Secret
                    │
                    ▼
              Shared Color
```

The application uses:

```python
socket
threading
```

for network communication and asynchronous receiving.

---

## 🔄 Complete Workflow

### Step 1 — Start the Server

On Laptop 1:

```text
Start as Server
```

The application starts a TCP server on:

```text
Port: 12345
```

The server displays its local IP address.

Example:

```text
Server running!

Your IP: 192.168.1.105
Port: 12345
Waiting for friend...
```

---

### Step 2 — Connect the Client

On Laptop 2, enter the server's IP address:

```text
192.168.1.105
```

Then select:

```text
Connect to Server
```

The client establishes a TCP connection:

```python
socket.connect(
    (server_ip, 12345)
)
```

---

### Step 3 — Choose Private Paint

Each user chooses a different private color.

For example:

```text
Alice → 🔴 Red

Bob → 🔵 Blue
```

The colors are local/private and are not used as the cryptographic secret.

---

### Step 4 — Generate DH Keys

Each computer generates a random private key:

```python
private_key = secrets.randbelow(
    DH_PRIME - 2
) + 2
```

The public key is calculated using:

```python
public_key = pow(
    DH_GENERATOR,
    private_key,
    DH_PRIME
)
```

Mathematically:

```text
A = g^a mod p
```

or:

```text
B = g^b mod p
```

---

### Step 5 — Exchange Public Keys

The public keys are sent through the TCP connection.

The transmitted message follows the format:

```text
PUBLIC_KEY:<public_key>
```

For example:

```text
PUBLIC_KEY:12345678901234567890...
```

The private key is **never sent**.

---

### Step 6 — Generate the Shared Secret

After receiving the other person's public key:

```python
shared_secret = pow(
    other_public_key,
    private_key,
    DH_PRIME
)
```

This gives:

```text
Alice:

K = B^a mod p
```

and:

```text
Bob:

K = A^b mod p
```

Both produce:

```text
K = g^(ab) mod p
```

---

### Step 7 — Generate Shared Paint

The shared secret is converted into an RGB color.

For example:

```text
Shared Secret
      ↓
      ↓
RGB = (164, 194, 129)
      ↓
#A4C281
      ↓
🎨 SHARED SECRET PAINT
```

Both computers should display the same color.

---

# 🖥️ Application Interface

The application provides a step-by-step interface:

```text
┌─────────────────────────────────────────┐
│     🔐 Diffie-Hellman Paint Exchange    │
├─────────────────────────────────────────┤
│                                         │
│ 1. Network Setup                        │
│                                         │
│ Server IP: [192.168.1.105]              │
│                                         │
│ [Start as Server] [Connect to Server]   │
│                                         │
│ 2. Public DH Parameters                 │
│                                         │
│ Generator: 2                            │
│ Prime: FFFFFF...                        │
│                                         │
│ 3. Choose Your Private Paint            │
│                                         │
│ [Pick Secret Color]                     │
│                                         │
│ 4. Generate Your DH Public Key          │
│                                         │
│ [Generate Public Key]                   │
│                                         │
│ 5. Exchange Public Keys                 │
│                                         │
│ [Send Public Key]                       │
│                                         │
│ 6. Generate Shared Secret               │
│                                         │
│ [Calculate Shared Secret]               │
│                                         │
│ 7. Shared Secret Paint                  │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │                                     │ │
│ │             🎨 #A4C281              │ │
│ │                                     │ │
│ │       SHARED SECRET PAINT           │ │
│ │                                     │ │
│ └─────────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

The interface is scrollable so all stages of the exchange can be accessed even on smaller screens.

---

## 🛠️ Technologies Used

| Technology     | Purpose                              |
| -------------- | ------------------------------------ |
| Python         | Core programming language            |
| Tkinter        | Graphical user interface             |
| Socket         | TCP network communication            |
| Threading      | Background network operations        |
| Secrets        | Secure random private-key generation |
| Diffie-Hellman | Cryptographic key exchange           |
| RGB / Hex      | Shared-secret visualization          |

---

## 📁 Project Structure

```text
diffie-hellman-paint-exchange/
│
├── main.py
└── README.md
```

### `main.py`

Contains:

* Tkinter GUI
* TCP server
* TCP client
* Diffie-Hellman implementation
* Public-key exchange
* Shared-secret generation
* RGB visualization

---

# 🚀 Installation

## Requirements

Python 3.8 or newer is recommended.

The project uses Python's standard library, so no external packages are required.

Check your Python version:

```bash
python --version
```

or:

```bash
python3 --version
```

---

## Clone the Repository

```bash
git clone https://github.com/IS-PKV/diffie-hellman-paint-exchange.git
```

Move into the project:

```bash
cd diffie-hellman-paint-exchange
```

Run:

```bash
python main.py
```

---

# 💻 Running on Two Laptops

Both laptops should be connected to the **same local network/Wi-Fi** for the simplest demonstration.

## Laptop 1 — Server

Run:

```bash
python main.py
```

Select:

```text
Start as Server
```

The application will display an IP address such as:

```text
192.168.1.105
```

Share this IP address with Laptop 2.

---

## Laptop 2 — Client

Run:

```bash
python main.py
```

Enter:

```text
192.168.1.105
```

in the **Server IP** field.

Select:

```text
Connect to Server
```

Once connected, both users can perform the Diffie-Hellman exchange.

---

# 🔐 Security Model

The project demonstrates the fundamental mathematics of Diffie-Hellman:

```text
Public:
    g
    p
    A
    B

Private:
    a
    b

Shared:
    K
```

The private keys are generated locally and are not transmitted over the network.

### What is transmitted?

Only the public key:

```text
PUBLIC_KEY:<value>
```

### What remains private?

```text
Private Key
```

### What is generated independently?

```text
Shared Secret
```

---

# ⚠️ Security Disclaimer

This project is intended for **educational and demonstration purposes**.

Although it implements the core Diffie-Hellman mathematical operation, it should **not be treated as a production-ready cryptographic system**.

A real secure communication system requires additional protections such as:

* Authentication
* Protection against man-in-the-middle attacks
* Secure key derivation
* Message encryption
* Message authentication/integrity
* Properly standardized cryptographic parameters
* Secure protocol design

For real-world applications, established cryptographic protocols and vetted libraries should be preferred over implementing cryptography manually.

---

# 🧪 Example Result

Suppose two laptops perform the exchange.

### Laptop 1

```text
Private Key:
<hidden>

Public Key:
<generated>

Friend's Public Key:
<received>

Shared Secret:
<generated>

Shared Paint:
#A4C281
```

### Laptop 2

```text
Private Key:
<hidden>

Public Key:
<generated>

Friend's Public Key:
<received>

Shared Secret:
<same value>

Shared Paint:
#A4C281
```

The important observation is:

```text
Laptop 1 Shared Secret
        =
Laptop 2 Shared Secret
```

and therefore:

```text
Laptop 1 Color
        =
Laptop 2 Color
```

---

# 📚 Learning Objectives

This project demonstrates practical concepts in:

* Public-key cryptography
* Diffie-Hellman key exchange
* Modular exponentiation
* TCP/IP networking
* Client-server architecture
* Socket programming
* Multithreading
* GUI development
* Cryptographically secure random number generation
* Data serialization and transmission
* Visualization of cryptographic concepts

---

# 🔮 Future Improvements

Potential extensions include:

* [ ] AES encryption using the derived shared key
* [ ] SHA-256 based Key Derivation Function
* [ ] Secure message exchange after key establishment
* [ ] Message authentication using HMAC
* [ ] Digital signatures for authentication
* [ ] Man-in-the-middle attack demonstration
* [ ] Attack simulation and visualization
* [ ] Chat functionality after key exchange
* [ ] Improved cryptographic parameter handling
* [ ] Network discovery for devices on the same LAN
* [ ] Exporting exchange logs for educational analysis

---

# 🎯 Educational Use

This project can be used as a demonstration for courses or projects involving:

* Cryptography
* Network Security
* Computer Networks
* Information Security
* Cybersecurity
* Python Networking
* Secure Communication

The paint metaphor makes the otherwise abstract Diffie-Hellman process easier to visualize and explain.

---

# 🤝 Contributing

Contributions, improvements, and educational extensions are welcome.

A typical workflow is:

```bash
git clone <repository>
```

Create a feature branch:

```bash
git checkout -b feature/new-feature
```

Make your changes, then:

```bash
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

Open a pull request on GitHub.

---

# 📄 License

This project is intended for educational purposes.

If you plan to publish the repository as an open-source project, add an appropriate license such as the MIT License.

---

# 👩‍💻 Author

**Preethi**

B.Tech — Civil Engineering
Minor — Computer Science
NIT Trichy

---

## ⭐ If you found this project useful

Consider giving the repository a ⭐ on GitHub and experimenting with the cryptographic exchange yourself!

