
# NetZero Lab 13 — EtherChannel with LACP

## 📌 Lab Overview

In this lab, I configured **EtherChannel using LACP (Link Aggregation Control Protocol)** between two Cisco switches.

EtherChannel combines multiple physical links into a single logical link called a **Port-channel**.

In this lab:

- Two FastEthernet links were bundled together.
- LACP was used to negotiate the EtherChannel.
- Port-channel 1 (Po1) was created.
- Both physical interfaces successfully joined the EtherChannel.
- The configuration was saved on both switches.

---

## 🎯 Objectives

- Understand EtherChannel.
- Configure EtherChannel using LACP.
- Configure multiple physical interfaces as an EtherChannel.
- Verify LACP operation.
- Verify Port-channel status.
- Troubleshoot a down EtherChannel member.
- Save the configuration to NVRAM.

---

## 🖥️ Topology

```text
                 LACP EtherChannel
              =======================
              ||                  ||
          Fa0/1                  Fa0/2
              ||                  ||
        +-------------+      +-------------+
        |    SW1      |------|    SW2      |
        +-------------+      +-------------+
              \                  /
               \                /
                \              /
              Port-channel 1
                   Po1
````

### EtherChannel Links

| SW1 Interface | SW2 Interface | Protocol |
| ------------- | ------------- | -------- |
| Fa0/1         | Fa0/1         | LACP     |
| Fa0/2         | Fa0/2         | LACP     |

Both physical links are combined into:

```text
Port-channel 1 (Po1)
```

---

# ⚙️ Configuration

## Step 1 — Configure SW1

Enter privileged EXEC mode:

```cisco
enable
configure terminal
```

Select the two physical interfaces:

```cisco
interface range fa0/1 - 2
```

Configure LACP:

```cisco
channel-group 1 mode active
```

Exit configuration mode:

```cisco
exit
exit
```

---

## Step 2 — Configure SW2

Enter privileged EXEC mode:

```cisco
enable
configure terminal
```

Select the two physical interfaces:

```cisco
interface range fa0/1 - 2
```

Configure LACP:

```cisco
channel-group 1 mode active
```

Exit configuration mode:

```cisco
exit
exit
```

---

# 🔍 Verification

## 1. Check EtherChannel Summary

Command:

```cisco
show etherchannel summary
```

### Final SW1 Output

```text
Group  Port-channel  Protocol    Ports
------+-------------+-----------+----------------
1      Po1(SU)       LACP        Fa0/1(P) Fa0/2(P)
```

### Output Interpretation

```text
Po1(SU)
```

* `S` = Layer 2 EtherChannel
* `U` = Port-channel is in use

```text
Fa0/1(P)
Fa0/2(P)
```

* `P` = Port is successfully bundled in the EtherChannel

```text
LACP
```

Confirms that LACP is being used.

---

## 2. Check Port-channel Interface

Command:

```cisco
show interfaces port-channel 1
```

### Verified Output

```text
Port-channel1 is up, line protocol is up (connected)
```

The output also confirmed:

```text
Members in this channel: Fa0/2 Fa0/1
```

This confirms that both physical interfaces are members of Port-channel 1.

---

## 3. Check Detailed EtherChannel Information

Command:

```cisco
show etherchannel port-channel
```

### Verified Information

```text
Port-channel: Po1 (Primary Aggregator)

Number of ports = 2

Protocol = LACP

Ports in the Port-channel:

Fa0/2    Active
Fa0/1    Active
```

This confirms:

* Port-channel 1 is the primary aggregator.
* Two physical ports are participating.
* LACP is active.
* Both interfaces are active members.

---

# 🛠️ Troubleshooting

Initially, the EtherChannel showed:

```text
Po1(SU)   LACP   Fa0/1(D) Fa0/2(P)
```

The problem was identified using:

```cisco
show interfaces fa0/1
```

The interface showed:

```text
FastEthernet0/1 is administratively down,
line protocol is down (disabled)
```

This indicated that Fa0/1 had been manually shut down.

### Solution

The interface was enabled using:

```cisco
enable
configure terminal
interface fa0/1
no shutdown
exit
exit
```

After enabling the interface, verification showed:

```text
Po1(SU)   LACP   Fa0/1(P) Fa0/2(P)
```

The EtherChannel was then fully operational.

---

# 💾 Save Configuration

The configuration was saved on both switches using:

```cisco
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

Expected result:

```text
Building configuration...
[OK]
```

---

# 📋 Important Commands

| Command                              | Purpose                                |
| ------------------------------------ | -------------------------------------- |
| `show etherchannel summary`          | View EtherChannel status               |
| `show interfaces port-channel 1`     | View Port-channel interface            |
| `show etherchannel port-channel`     | View detailed EtherChannel information |
| `show interfaces fa0/1`              | Check physical interface status        |
| `show running-config`                | View current configuration             |
| `show startup-config`                | View saved configuration               |
| `copy running-config startup-config` | Save configuration                     |

---

# 🧠 Key Concepts Learned

### EtherChannel

EtherChannel combines multiple physical links into one logical link.

Instead of treating:

```text
Fa0/1
Fa0/2
```

as two separate links, the switch treats them as:

```text
Po1
```

---

### LACP

**LACP — Link Aggregation Control Protocol**

LACP dynamically negotiates the formation of an EtherChannel.

The configuration used:

```cisco
channel-group 1 mode active
```

`active` means the switch actively participates in LACP negotiation.

---

### Port-channel

A Port-channel is the logical interface created from the bundled physical interfaces.

In this lab:

```text
Po1
```

represents:

```text
Fa0/1 + Fa0/2
```

---

# ✅ Final Verification

Final EtherChannel status:

```text
Group  Port-channel  Protocol    Ports
------+-------------+-----------+----------------
1      Po1(SU)       LACP        Fa0/1(P) Fa0/2(P)
```

Port-channel status:

```text
Port-channel1 is up,
line protocol is up (connected)
```

Detailed LACP status:

```text
Number of ports = 2
Protocol = LACP

Fa0/2    Active
Fa0/1    Active
```

---

# 🏆 Lab Result

**NetZero Lab 13 successfully completed.**

I successfully configured and verified a **Layer 2 EtherChannel using LACP** between two Cisco switches.

The final configuration successfully bundled **Fa0/1 and Fa0/2 into Port-channel 1**, with both interfaces operating as active LACP members.

---

## 📚 Skills Demonstrated

* Cisco IOS configuration
* EtherChannel configuration
* LACP
* Link aggregation
* Port-channel configuration
* Interface troubleshooting
* Network redundancy
* Layer 2 switching
* Cisco Packet Tracer
* Network verification
* Configuration backup

---

## 🔑 Technologies

* Cisco Switches
* Cisco IOS
* Cisco Packet Tracer
* EtherChannel
* LACP
* Layer 2 Switching

---

