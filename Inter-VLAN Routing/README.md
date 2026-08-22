## 📌 Overview

This lab demonstrates **Inter-VLAN Routing using a Cisco Layer 3 Multilayer Switch**.

Unlike traditional Router-on-a-Stick configuration, this lab uses **Switched Virtual Interfaces (SVIs)** on a Cisco 3560 multilayer switch to provide default gateways for different VLANs.

The multilayer switch performs both:

* Layer 2 switching
* Layer 3 routing

The `ip routing` command enables Layer 3 routing on the multilayer switch, while SVIs provide the Layer 3 gateway for each VLAN.

---

## 🎯 Objectives

* Create VLANs on a multilayer switch
* Assign switch ports to VLANs
* Configure SVIs
* Assign IP addresses to SVIs
* Enable Layer 3 IP routing
* Configure PCs in different VLANs
* Configure default gateways
* Verify the routing table
* Test communication between different VLANs

---

## 🖥️ Topology

```text
                    ┌─────────────────────────┐
                    │     3560 Multilayer     │
                    │         Switch          │
                    │                         │
                    │  VLAN 10 → 192.168.10.1 │
                    │  VLAN 20 → 192.168.20.1 │
                    └───────────┬─────────────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
              Fa0/1                       Fa0/2
                  │                           │
                PC1                         PC0
              VLAN 10                    VLAN 20
               SALES                       IT
```

---

## 🔌 Devices Used

| Device            | Model                   | Quantity |
| ----------------- | ----------------------- | -------: |
| Multilayer Switch | Cisco 3560-24PS         |        1 |
| PC                | PC-PT                   |        2 |
| Cable             | Copper Straight-Through |        2 |

---

## 🌐 IP Addressing Table

| Device    | Interface     | VLAN | IP Address    | Subnet Mask   | Default Gateway |
| --------- | ------------- | ---: | ------------- | ------------- | --------------- |
| PC1       | FastEthernet0 |   10 | 192.168.10.10 | 255.255.255.0 | 192.168.10.1    |
| PC0       | FastEthernet0 |   20 | 192.168.20.10 | 255.255.255.0 | 192.168.20.1    |
| L3 Switch | VLAN 10       |   10 | 192.168.10.1  | 255.255.255.0 | —               |
| L3 Switch | VLAN 20       |   20 | 192.168.20.1  | 255.255.255.0 | —               |

---

# ⚙️ Configuration

## Step 1 — Create VLANs

Enter the following commands on the multilayer switch:

```text
enable
configure terminal

vlan 10
name SALES
exit

vlan 20
name IT
exit
```

---

## Step 2 — Configure Access Ports

Assign PC1 to VLAN 10:

```text
interface fastEthernet 0/1
switchport mode access
switchport access vlan 10
exit
```

Assign PC0 to VLAN 20:

```text
interface fastEthernet 0/2
switchport mode access
switchport access vlan 20
exit
```

---

## Step 3 — Configure SVI for VLAN 10

```text
interface vlan 10
ip address 192.168.10.1 255.255.255.0
no shutdown
exit
```

The VLAN 10 SVI acts as the default gateway for devices in the SALES VLAN.

---

## Step 4 — Configure SVI for VLAN 20

```text
interface vlan 20
ip address 192.168.20.1 255.255.255.0
no shutdown
exit
```

The VLAN 20 SVI acts as the default gateway for devices in the IT VLAN.

An SVI provides the Layer 3 interface associated with its VLAN and can be used for routing between VLANs on a multilayer switch.

---

## Step 5 — Enable Layer 3 Routing

```text
ip routing
exit
```

Save the configuration:

```text
copy running-config startup-config
```

When prompted:

```text
Destination filename [startup-config]?
```

Press:

```text
Enter
```

The `ip routing` command enables IPv4 routing on the multilayer switch.

---

# 💻 PC Configuration

## PC1 — SALES VLAN

Go to:

**PC1 → Desktop → IP Configuration**

Enter:

```text
IP Address:      192.168.10.10
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.10.1
```

---

## PC0 — IT VLAN

Go to:

**PC0 → Desktop → IP Configuration**

Enter:

```text
IP Address:      192.168.20.10
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.20.1
```

---

# 🔍 Verification Commands

## 1. Verify VLANs

```text
show vlan brief
```

Expected:

```text
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active
10   SALES                            active    Fa0/1
20   IT                               active    Fa0/2
```

---

## 2. Verify SVI Interfaces

```text
show ip interface brief
```

Expected relevant output:

```text
Vlan10    192.168.10.1    YES manual    up    up
Vlan20    192.168.20.1    YES manual    up    up
```

---

## 3. Verify IP Routing

```text
show running-config | include ip routing
```

Expected:

```text
ip routing
```

---

## 4. Verify Routing Table

```text
show ip route
```

Expected connected routes:

```text
C    192.168.10.0/24
C    192.168.20.0/24
```

The two VLAN networks appear as directly connected routes because their SVIs are configured on the multilayer switch.

---

## 5. Verify VLAN Configuration

```text
show running-config
```

Check for:

```text
vlan 10
 name SALES

vlan 20
 name IT

interface Vlan10
 ip address 192.168.10.1 255.255.255.0

interface Vlan20
 ip address 192.168.20.1 255.255.255.0

ip routing
```

---

# 🧪 Connectivity Testing

## Test 1 — PC1 to its Gateway

From PC1:

```text
ping 192.168.10.1
```

Expected:

```text
Packets: Sent = 4, Received = 4, Lost = 0
```

---

## Test 2 — PC0 to its Gateway

From PC0:

```text
ping 192.168.20.1
```

Expected:

```text
Packets: Sent = 4, Received = 4, Lost = 0
```

---

## Test 3 — Inter-VLAN Communication

From PC1:

```text
ping 192.168.20.10
```

Expected:

```text
Packets: Sent = 4, Received = 4, Lost = 0
```

This confirms that traffic is successfully being routed from:

```text
VLAN 10
192.168.10.0/24
        ↓
192.168.10.1
        ↓
Layer 3 Switch
        ↓
192.168.20.1
        ↓
VLAN 20
192.168.20.0/24
```

---

## Test 4 — Reverse Communication

From PC0:

```text
ping 192.168.10.10
```

Expected:

```text
Packets: Sent = 4, Received = 4, Lost = 0
```

---

# 🔄 How Inter-VLAN Routing Works

PC1 belongs to:

```text
VLAN 10
IP: 192.168.10.10
Gateway: 192.168.10.1
```

PC0 belongs to:

```text
VLAN 20
IP: 192.168.20.10
Gateway: 192.168.20.1
```

When PC1 sends traffic to PC0:

```text
PC1
192.168.10.10
       |
       v
VLAN 10
       |
       v
SVI VLAN 10
192.168.10.1
       |
       v
Layer 3 Routing
       |
       v
SVI VLAN 20
192.168.20.1
       |
       v
VLAN 20
       |
       v
PC0
192.168.20.10
```

The multilayer switch performs the routing between the two VLANs. Cisco documents SVIs as the Layer 3 interfaces used to provide routing between VLANs on multilayer switches.

---

# 🆚 Router-on-a-Stick vs Layer 3 Switch

| Feature          | Router-on-a-Stick      | Layer 3 Switch      |
| ---------------- | ---------------------- | ------------------- |
| Routing Device   | Router                 | Multilayer Switch   |
| VLAN Gateway     | Router Subinterface    | SVI                 |
| `ip routing`     | Not required on router | Required            |
| External Router  | Required               | Not required        |
| Routing Location | Router                 | Switch              |
| Typical Use      | Small networks/labs    | Enterprise LANs     |
| Example          | `G0/0.10`              | `interface vlan 10` |

---

# 🛠️ Troubleshooting

### Problem: SVI is down

Check:

```text
show ip interface brief
```

Make sure the VLAN exists:

```text
show vlan brief
```

Make sure at least one active Layer 2 port belongs to that VLAN. An SVI generally needs an active port/trunk in its VLAN to come up.

---

### Problem: PC cannot ping another VLAN

Check:

```text
show ip interface brief
show ip route
show running-config | include ip routing
```

Verify:

* PC IP address
* Subnet mask
* Default gateway
* VLAN assignment
* SVI IP address
* `ip routing`

---

### Problem: VLAN is missing

Create it again:

```text
configure terminal

vlan 10
name SALES
exit

vlan 20
name IT
exit
```
