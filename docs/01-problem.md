---
doc_id: FXH-PRB-001
title: FlexHand problem statement
project: FlexHand
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, prior work)
---

# FlexHand problem statement

Recovery of hand function after stroke seems to depend on a large number of movement repetitions, but a typical therapy session delivers only a few dozen, and the rest of the day the affected hand often stays still and curled into flexion. FlexHand is a low-cost, open, wearable device that moves the fingers through hundreds of controlled flexion and extension cycles a day at home, within limits a therapist sets.

## The problem

Hand impairment is common and persistent after stroke. In a cohort of people who had a flaccid arm soon after stroke, only about 38 % had regained some dexterity at six months ([Kwakkel et al., *Stroke*, 2003](https://www.ahajournals.org/doi/full/10.1161/01.STR.0000087172.16305.CD)). Difficulty opening the hand is a large part of this impairment: finger extension deficits after stroke arise from both neural factors and changed muscle mechanics ([Kamper and Rymer, *Muscle & Nerve*, 2003](https://onlinelibrary.wiley.com/doi/10.1002/mus.10443)), and finger extension is typically affected more than flexion ([Soft pneumatic actuators for pushing fingers into extension, *JNER*, 2024](https://link.springer.com/article/10.1186/s12984-024-01444-4)).

Therapy dose is small. Lang and colleagues observed 312 physical and occupational therapy sessions and found an average of 32 repetitions of upper-limb functional movement per session, against the 400 to 600 repetitions per session used in animal models of recovery ([Lang et al., *Archives of Physical Medicine and Rehabilitation*, 2009](https://www.archives-pmr.org/article/S0003-9993(09)00353-0/abstract); [full text](https://epublications.marquette.edu/cgi/viewcontent.cgi?httpsredir=1&article=1073&context=phys_therapy_fac)). Therapist time is the limit, not the patient's day.

Devices that move the hand exist, but they are costly, clinic-bound or closed:

- Clinical robotic gloves such as Gloreha Sinfonia (now BTL R-TOUCH PRO) offer passive and active-assisted finger training, but they are tethered clinic systems ([Exoskeleton Report](https://exoskeletonreport.com/product/gloreha-sinfonia/)).
- The NEOFECT Smart Glove costs about $2,000 and tracks active movement for games; it does not move a hand that cannot move itself ([Recovery After Stroke](https://recoveryafterstroke.com/neofect-hand-rehabilitation/)).
- Research tendon-driven gloves show the approach works. The Columbia hand orthosis for stroke uses a single forearm-mounted gearmotor with about 100 N peak tendon force and a dorsal tendon network to extend four fingers ([Park et al., arXiv 1802.06131](https://arxiv.org/abs/1802.06131); [ROAM Lab](https://roam.me.columbia.edu/research-projects/hand-orthosis-stroke-rehabilitation)). Exo-Glove Poly II uses one actuator with antagonistic tendons and a 104 g polymer glove, but its actuation unit weighs about 1.14 kg and sits on a desk or wheelchair ([Kang et al., *Soft Robotics*, 2019](https://journals.sagepub.com/doi/10.1089/soro.2018.0006)).

No open, garage-buildable, wearable design exists that a clinic, a research group or a family can build, inspect and adapt for daily repetitive finger movement at home.

A caution sits at the center of this problem. Robotic passive mobilization has been studied mainly for short-term effects on spasticity and limb perfusion ([Hand Passive Mobilization Performed with Robotic Assistance, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC5637828/)). Whether passive repetitions alone improve hand function is not established. FlexHand therefore starts as a passive-motion device that can later add active or intent-triggered modes, and it makes no therapeutic claim.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Stroke survivor with moderate hand impairment (subacute or chronic) | Many gentle, repeatable finger movements a day without waiting for a therapist | Home, seated with the forearm resting on a table or pillow; 30 to 60 min sessions, one to three a day |
| Care partner | Put the device on and take it off quickly and safely; know what to do if something goes wrong | Home |
| Occupational or physical therapist | Set range-of-motion, speed and force limits; see how many cycles were done | Clinic visit, then remote review |
| Researcher or open hardware community | A documented, reproducible platform to study dose and control strategies | University labs, makerspaces |

## Constraints

- Garage-buildable prototype for about $500 USD in parts, using off-the-shelf motors and modules and 3D-printed parts.
- Wearable during a seated session: the hand side must be light and the actuators must sit on the forearm, not the hand.
- Fits a range of adult hands without custom molding.
- Safe with users who may have reduced sensation, spasticity and limited ability to remove the device themselves.
- Research and educational use only. FlexHand is not a medical device, has not been cleared or approved by any regulator, and must not be used to diagnose or treat any person outside a supervised research setting.

> **Safety:** The device applies force to joints that may be spastic, contracted or insensate, and it carries a lithium-ion battery. Force limits, a physical stop, a tool-free tendon release and supervised use are part of the problem definition, not extras.

## Out of scope

- Thumb actuation (the thumb is held in a passive abducted position in this concept).
- Wrist actuation.
- Diagnosis, assessment scoring or any therapeutic claim.
- Cloud services.

## Open questions

- Which clinical partner to co-design with first (a stroke unit occupational therapy team, a community rehabilitation service, or a university rehabilitation lab)? Proposed, awaiting Amish.
- Passive motion only, or plan from the start for an active-assist mode triggered by the user's own effort? This affects the pitch. Proposed, awaiting Amish.
- Which severity band to design for first (mild to moderate flexor tone is assumed)? Proposed, awaiting Amish.
