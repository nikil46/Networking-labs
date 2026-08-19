# NetZero Lab 12 — Inter-VLAN Routing Using Layer 3 Switch

````markdown
# 🚀 NetZero Lab 12 — Inter-VLAN Routing Using Layer 3 Switch

## 📌 Objective

The objective of this lab is to configure **Inter-VLAN Routing using a Layer 3 Multilayer Switch** in Cisco Packet Tracer.

In this lab, a Cisco 3560 Multilayer Switch is configured to perform routing between:

- VLAN 10 — SALES
- VLAN 20 — IT

The lab demonstrates how a Layer 3 switch can route traffic between different VLANs without using a dedicated router.

---

## 🛠️ Tools Used

- Cisco Packet Tracer
- Cisco 3560-24PS Multilayer Switch
- Cisco 2960 Switch × 2
- PCs × 4

---

## 🧩 Network Topology

```text
                 ┌───────────────────┐
                 │       MLS1        │
                 │ Cisco 3560-24PS   │
                 │  Layer 3 Switch   │
                 └───────┬─────┬─────┘
                         │     │
                    Trunk│     │Trunk
                         │     │
                    ┌────┘     └────┐
                    │               │
              ┌─────┴─────┐   ┌─────┴─────┐
              │    SW1    │   │    SW2    │
              │  Cisco    │   │  Cisco    │
              │   2960    │   │   2960    │
              └──┬─────┬──┘   └──┬─────┬──┘
                 │     │           │     │
                PC0   PC1         PC2   PC3
               VLAN10 VLAN20     VLAN10 VLAN20
````

---

## 🔌 Connections

| Device | Interface | Connected To | Interface |
| ------ | --------- | ------------ | --------- |
| MLS1   | Gi0/1     | SW1          | Gi0/1     |
| MLS1   | Gi0/2     | SW2          | Gi0/1     |
| SW1    | Fa0/1     | PC0          | NIC       |
| SW1    | Fa0/2     | PC1          | NIC       |
| SW2    | Fa0/1     | PC2          | NIC       |
| SW2    | Fa0/2     | PC3          | NIC       |

---

## 🌐 VLAN Configuration

| VLAN ID | VLAN Name | Network         | Default Gateway |
| ------- | --------- | --------------- | --------------- |
| 10      | SALES     | 192.168.10.0/24 | 192.168.10.1    |
| 20      | IT        | 192.168.20.0/24 | 192.168.20.1    |

---

## 💻 IP Addressing Table

| Device | VLAN | IP Address    | Subnet Mask   | Default Gateway |
| ------ | ---: | ------------- | ------------- | --------------- |
| PC0    |   10 | 192.168.10.10 | 255.255.255.0 | 192.168.10.1    |
| PC1    |   20 | 192.168.20.10 | 255.255.255.0 | 192.168.20.1    |
| PC2    |   10 | 192.168.10.20 | 255.255.255.0 | 192.168.10.1    |
| PC3    |   20 | 192.168.20.20 | 255.255.255.0 | 192.168.20.1    |

---

# ⚙️ Configuration

## 1. Configure VLANs on SW1

```text
enable
configure terminal

vlan 10
name SALES
exit

vlan 20
name IT
exit

interface fastEthernet 0/1
switchport mode access
switchport access vlan 10
exit

interface fastEthernet 0/2
switchport mode access
switchport access vlan 20
exit

end
```

### Verify SW1

```text
show vlan brief
```

Expected:

```text
10   SALES    active    Fa0/1
20   IT       active    Fa0/2
```

---

## 2. Configure VLANs on SW2

```text
enable
configure terminal

vlan 10
name SALES
exit

vlan 20
name IT
exit

interface fastEthernet 0/1
switchport mode access
switchport access vlan 10
exit

interface fastEthernet 0/2
switchport mode access
switchport access vlan 20
exit

end
```

### Verify SW2

```text
show vlan brief
```

Expected:

```text
10   SALES    active    Fa0/1
20   IT       active    Fa0/2
```

---

# 🔗 3. Configure Trunk on SW1

```text
enable
configure terminal

interface gigabitEthernet 0/1
switchport mode trunk
exit

end
```

Verify:

```text
show interfaces trunk
```

Expected:

```text
Gig0/1    trunking
```

---

# 🔗 4. Configure Trunk on SW2

```text
enable
configure terminal

interface gigabitEthernet 0/1
switchport mode trunk
exit

end
```

Verify:

```text
show interfaces trunk
```

Expected:

```text
Gig0/1    trunking
```

---

# 🔗 5. Configure Trunk Ports on MLS1

```text
enable
configure terminal

interface gigabitEthernet 0/1
switchport mode trunk
exit

interface gigabitEthernet 0/2
switchport mode trunk
exit

end
```

Verify:

```text
show interfaces trunk
```

Expected:

```text
Gig0/1    trunking
Gig0/2    trunking
```

---

# 🧠 6. Configure VLANs on MLS1

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

# 🌐 7. Configure SVI for VLAN 10

```text
interface vlan 10
ip address 192.168.10.1 255.255.255.0
no shutdown
exit
```

---

# 🌐 8. Configure SVI for VLAN 20

```text
interface vlan 20
ip address 192.168.20.1 255.255.255.0
no shutdown
exit
```

---

# 🚦 9. Enable Layer 3 Routing

This is the most important configuration on the multilayer switch.

```text
ip routing
end
```

The `ip routing` command enables the Cisco 3560 switch to perform Layer 3 routing between VLANs.

---

# 🔍 Verification

## Verify IP Interfaces

On MLS1:

```text
show ip interface brief
```

Expected:

```text
GigabitEthernet0/1     unassigned      up    up
GigabitEthernet0/2     unassigned      up    up
Vlan10                 192.168.10.1    up    up
Vlan20                 192.168.20.1    up    up
```

---

## Verify VLANs

```text
show vlan brief
```

Expected:

```text
10   SALES    active
20   IT       active
```

---

## Verify Trunk Ports

```text
show interfaces trunk
```

Expected:

```text
Gig0/1    trunking
Gig0/2    trunking
```

The trunk links allow VLAN 10 and VLAN 20 traffic to travel between the switches and MLS1.

---

## Verify Layer 3 Routing

```text
show running-config | include ip routing
```

Expected:

```text
ip routing
```

---

## Verify Routing Table

```text
show ip route
```

Expected connected routes:

```text
C    192.168.10.0/24
C    192.168.20.0/24
```

These routes confirm that the Layer 3 switch knows both VLAN networks directly through its SVIs.

---

# 🖥️ PC Configuration

## PC0

```text
IP Address:      192.168.10.10
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.10.1
```

## PC1

```text
IP Address:      192.168.20.10
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.20.1
```

## PC2

```text
IP Address:      192.168.10.20
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.10.1
```

## PC3

```text
IP Address:      192.168.20.20
Subnet Mask:     255.255.255.0
Default Gateway: 192.168.20.1
```

---

# 🧪 Connectivity Testing

## Test 1 — PC0 to PC2

Both PCs belong to VLAN 10.

From PC0:

```text
ping 192.168.10.20
```

Result:

```text
Packets: Sent = 4
Packets: Received = 4
Lost = 0
```

✅ VLAN 10 connectivity successful.

---

## Test 2 — PC1 to PC3

Both PCs belong to VLAN 20.

From PC1:

```text
ping 192.168.20.20
```

Expected:

```text
Packets: Sent = 4
Packets: Received = 4
Lost = 0
```

✅ VLAN 20 connectivity successful.

---

## Test 3 — Inter-VLAN Routing

From PC0:

```text
ping 192.168.20.10
```

PC0 is in VLAN 10 and PC1 is in VLAN 20.

Expected:

```text
Packets: Sent = 4
Packets: Received = 4
Lost = 0
```

✅ Inter-VLAN routing successful.

---

## Test 4 — Reverse Inter-VLAN Routing

From PC1:

```text
ping 192.168.10.10
```

Expected:

```text
Packets: Sent = 4
Packets: Received = 4
Lost = 0
```

✅ Reverse inter-VLAN connectivity successful.

---

# 📊 Verification Summary

| Test                    | Expected Result | Status |
| ----------------------- | --------------- | ------ |
| VLAN 10 configuration   | SALES active    | ✅      |
| VLAN 20 configuration   | IT active       | ✅      |
| SW1 trunk               | Trunking        | ✅      |
| SW2 trunk               | Trunking        | ✅      |
| MLS1 trunk              | Trunking        | ✅      |
| SVI VLAN 10             | Up/Up           | ✅      |
| SVI VLAN 20             | Up/Up           | ✅      |
| Layer 3 routing         | Enabled         | ✅      |
| VLAN 10 connectivity    | 4/4 received    | ✅      |
| VLAN 20 connectivity    | 4/4 received    | ✅      |
| Inter-VLAN connectivity | 4/4 received    | ✅      |

---

# 🧠 Skills Learned

Through this lab, I learned:

* VLAN creation and configuration
* VLAN naming
* Access port configuration
* Trunk port configuration
* 802.1Q trunking
* Layer 3 switch configuration
* Switched Virtual Interfaces (SVIs)
* Inter-VLAN routing
* `ip routing`
* IPv4 addressing
* Default gateway configuration
* Routing table verification
* VLAN troubleshooting
* Trunk verification
* End-to-end connectivity testing
* Cisco IOS commands
* Network troubleshooting

# 🎯 Final Result

The NetZero Lab 12 network was successfully configured using a **Cisco 3560 Multilayer Switch**.

VLAN 10 and VLAN 20 were created and configured across two access switches. Trunk links were established between the access switches and the multilayer switch. SVIs were configured on MLS1 and Layer 3 routing was enabled using `ip routing`.

Successful ping tests with:

```text
Sent = 4
Received = 4
Lost = 0
```

confirmed successful **inter-VLAN communication and end-to-end network connectivity**.
