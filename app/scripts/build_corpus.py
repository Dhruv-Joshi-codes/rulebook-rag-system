import os
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CORPUS_DIR = os.path.join(BASE_DIR, "corpus")
os.makedirs(CORPUS_DIR, exist_ok=True)

# 1. Academic Regulations
academic_regulations = """# Apex Institute of Technology & Higher Sciences
## Academic Regulations and Degree Governance Charter (Volume IV)

### Section 1: Institutional Foundation and Matriculation Standing
#### Clause 1.1: Scope of Academic Jurisdiction
These regulations govern all undergraduate degree programmes, integrated honours tracks, and dual-award curricula administered by the Academic Council of the Apex Institute of Technology & Higher Sciences. Every candidate enrolled in an academic programme undertakes to observe and abide by these statutes from the date of initial registration until formal degree conferral, transfer, or termination of candidature. The provisions herein apply across all instructional faculties, including the School of Computing, the School of Engineering, the School of Management Sciences, and the School of Applied Natural Sciences.

#### Clause 1.2: Matriculation Qualifications and Verification
Candidates admitted to the Institute must produce certified original documentation of qualifying examinations, secondary school transcripts, national examination scorecards, state certificates, and identity credentials within fourteen (14) calendar days of term commencement. Failure to present authentic credentials will result in summary provisional de-registration without recourse to tuition refund. In cases where foreign credentials require national equivalency validation, the Office of Academic Admissions may issue a provisional registration clearance valid for a non-renewable maximum window of thirty (30) calendar days.

#### Clause 1.3: Academic Advisors and Mentorship Assignment
Each matriculated student is assigned a designated Faculty Academic Advisor upon initial enrollment. Students are required to consult their Faculty Academic Advisor prior to final course selection, add/drop registration alterations, course withdrawal filings, and overload petitions. Advisor endorsement is an indispensable prerequisite for all formal academic filings lodged through the student portal. Advisors maintain regular consultation hours and review midterm academic alerts issued by course instructors.

### Section 2: Course Registration, Credit Loads, and Prerequisites
#### Clause 2.1: Standard Credit Load Limits
The standard semester credit load for full-time undergraduate students is eighteen (18) European Credit Transfer and Accumulation System (ECTS) credits or equivalent credit hours. A normal full-time schedule may not fall below twelve (12) credits nor exceed twenty-two (22) credits in any standard Autumn or Spring semester, except where an explicit academic overload petition has been formally ratified by the Academic Dean. Students registered for fewer than twelve (12) credits are designated part-time students and lose priority residential housing eligibility.

#### Clause 2.2: Academic Overload Criteria
A student with a Cumulative Grade Point Average (CGPA) of 3.60 or higher and no outstanding failed or incomplete grades from previous terms may petition for an academic overload up to twenty-six (26) credits. Such petitions require the joint signature of the Department Chair and the Academic Dean, and must be submitted within the initial three (3) days of the semester registration window. First-year undergraduate students in their initial two semesters of study are strictly ineligible for academic overloads regardless of secondary school academic credentials.

#### Clause 2.3: Prerequisite Sequencing and Waivers
No student may enroll in an advanced course without passing all designated prerequisite courses with a minimum letter grade of 'C' (2.00 grade point). Automatic waiver of prerequisites is strictly prohibited. In exceptional cases of demonstrable mastery, a Departmental Standing Board may administer a comprehensive challenge examination prior to the start of instruction. If a student passes the challenge exam with at least 80%, prerequisite status is marked as satisfied, although no course credits are awarded toward graduation.

#### Clause 2.4: Course Add and Drop Period
Students may freely alter their course registrations through the self-service academic portal during the first seven (7) calendar days of each regular semester. Any course dropped during this initial drop window will not appear on the student's official or unofficial academic transcript. Adding a course after Day 5 requires the written permission of the course instructor to ensure missed introductory lectures and safety orientations are adequately remedied.

### Section 3: Assessment Structures, Grading Scales, and Transcripts
#### Clause 3.1: 4.0 Grading Matrix
Academic performance across all undergraduate modular courses is evaluated and converted into quality points using a standard four-point (4.00) grading matrix defined as follows:
- Grade 'A+' (4.00): Outstanding scholarship, mastery of material exceeding 95% evaluation threshold.
- Grade 'A' (4.00): Superior mastery, demonstrated critical synthesis and problem solving between 90% and 94.9%.
- Grade 'A-' (3.70): Excellent execution of foundational and applied course objectives (85%-89.9%).
- Grade 'B+' (3.30): High competence, well above average satisfactory benchmark (80%-84.9%).
- Grade 'B' (3.00): Good competence, standard satisfactory benchmark across assignments (75%-79.9%).
- Grade 'B-' (2.70): Adequate comprehension with minor analytical or technical deficiencies (70%-74.9%).
- Grade 'C+' (2.30): Minimally competent, baseline acceptable pass for core degree requirements (65%-69.9%).
- Grade 'C' (2.00): Lowest qualifying grade for prerequisite satisfaction and major progression (60%-64.9%).
- Grade 'D' (1.00): Marginal credit awarded; counts towards total credits but cannot satisfy major prerequisite conditions (50%-59.9%).
- Grade 'F' (0.00): Total failure; no credit awarded; compulsory repetition required for core graduation courses.

#### Clause 3.2: Incomplete Grades ('I' Designation)
An Incomplete grade ('I') may be recorded exclusively at the discretion of the course instructor when a student, through documented severe medical incapacitation or tragic family calamity occurring in the final two weeks of the term, has been prevented from completing the final assessment or submitting the capstone assignment. The student must have maintained satisfactory academic progress (minimum grade of 'C' across pre-final assessments) prior to the intervening calamity. An Incomplete grade must be resolved into a standard letter grade within forty-five (45) calendar days of the subsequent semester start; otherwise, the 'I' mark converts automatically and irreversibly to a failing grade ('F').

#### Clause 3.3: Grade Disputes and Formal Re-evaluation
A student may challenge an assigned final course grade by lodging a formal petition with the Dean of Examinations within ten (10) working days following official transcript publication. The petition must be accompanied by an administrative review fee of $75 and tangible evidence of arithmetic inaccuracy, capricious evaluation, or demonstrable deviation from the published course syllabus grading scheme. An independent three-member faculty review panel convenes within twenty (20) working days; if the dispute is upheld in the student's favor, the grade is formally corrected and the $75 deposit is fully refunded.

### Section 4: Attendance Regulations and Examination Qualification
#### Clause 4.1: Continuous Academic Engagement
Regular attendance in lectures, interactive seminars, computer laboratory practicals, and clinical tutorials is a mandatory pedagogical foundation of the curriculum. Instructors must take roll call or register digital attendance via biometric checkpoints at each scheduled class contact hour. Faculty members are mandated to publish cumulative attendance figures on the internal student portal every fortnight.

#### Clause 4.2: Mandatory 75% Examination Attendance Threshold [PLANTED CONTRADICTION 1A]
(a) A student must maintain a minimum of 75% attendance across lectures, tutorials, and laboratory practicals in each registered course to be eligible to sit the end-semester examinations. This requirement is strictly mandatory; no exceptions, waivers, or leaves shall be granted under any circumstance, and any student below 75% shall automatically receive an examination debarment notice.
(b) Students issued an examination debarment notice under Section 4.2(a) are classified as 'Debarred for Low Attendance' (code 'DA') and must re-register and re-pay tuition for the entire course in a subsequent academic term.

#### Clause 4.3: Computation Methodology for Attendance Percentage
Attendance percentages are calculated by dividing the total number of class periods attended by the total number of scheduled contact hours from Day 1 of instruction to the final official instructional day of the semester. Periods missed due to late registration, personal travel, extracurricular sports, club festivals, or unexcused absences are counted strictly as missed instructional periods. Where an instructor cancels a class and conducts a makeup session, attendance at the makeup session replaces the original lecture in the denominator.

### Section 5: Examination Conduct, Protocols, and Invigilation
#### Clause 5.1: Admission to the Examination Hall
Candidates must report to the examination hall at least twenty (20) minutes prior to the scheduled exam commencement. Entry into the examination room will not be permitted after thirty (30) minutes have elapsed from the start of the paper. No candidate may leave the hall during the first forty-five (45) minutes or during the final fifteen (15) minutes of the examination session. Candidates leaving the hall temporarily for restroom visits must be escorted by an authorized proctor and may not possess any personal belongings.

#### Clause 5.2: Approved Examination Stationery and Writing Implements
Candidates are authorized to bring only designated writing instruments into the hall, specifically black and dark blue ballpoint or indelible ink pens, non-programmable scientific calculators (without wireless transmission capabilities), wooden rulers, and clear plastic water bottles with all commercial paper labels removed. All stationery items must be held within a transparent PVC pencil pouch. Any writing implement not explicitly mentioned herein is prohibited inside the testing room.

#### Clause 5.3: Prohibited Items and Communication Equipment
Mobile telephones, cellular watches, smart earbuds, electronic computing devices, programmable watches, slide rules, scrap paper, annotated textbooks, and wearable recording devices are strictly prohibited inside the examination center. Possession of unauthorized electronic equipment inside the exam perimeter constitutes prima facie evidence of academic malpractice, resulting in immediate confiscation and referral to the Proctorial Board.

#### Clause 5.4: Examination Accommodation for Students with Disabilities
Students with registered physical disabilities, chronic medical ailments, or verified visual impairments registered with the Disability Support Office are entitled to specified examination accommodations, including twenty (20) additional minutes per examination hour and the provision of a certified amanuensis (scribe) appointed by the Office of the Registrar. Scribes may not possess formal qualifications or degrees in the academic subject matter being tested. Requests for disability accommodations must be renewed annually before Week 3 of the Autumn semester.

### Section 6: Course Withdrawals and Tuition Adjustments
#### Clause 6.1: Voluntary Course Withdrawal Procedure
Following the conclusion of the initial Add/Drop period, a student may voluntarily withdraw from a course by submitting a Course Withdrawal Form endorsed by the Course Instructor and Academic Advisor through the academic portal. Withdrawals logged between Day 8 and Day 28 are designated with a 'W' mark on the student's permanent transcript. The 'W' mark does not affect the calculation of the semester or cumulative Grade Point Average.

#### Clause 6.2: Final Deadline for Course Withdrawal
No course withdrawal will be permitted after the conclusion of Week 9 (Day 63 of the semester instruction calendar). Any student who discontinues attending class or fails to complete assessments after Week 9 without an authorized leave of absence will receive the earned letter grade, including zero points for missed final evaluations. A maximum of four (4) 'W' grades are allowed throughout an entire undergraduate degree.

#### Clause 6.3: Course Drop Tuition Refund Schedule [PLANTED CONTRADICTION 3A]
Any student who officially drops or withdraws from a semester course prior to the conclusion of Week 4 (Day 28 of the semester instruction calendar) through the student academic portal is entitled to an eighty percent (80%) prorated tuition fee refund for the credits associated with that course. Refunds will be credited to the student's institutional account within twenty-one (21) banking days of the processed withdrawal.

### Section 7: Academic Integrity and Research Misconduct
#### Clause 7.1: Plagiarism and Academic Deception
Academic fraud, plagiarism, collusion, duplicate submission of work across distinct modules, unauthorized collaboration on take-home examinations, fabrication of empirical lab data, and commissioning external entities or AI synthesis tools to complete coursework without explicit syllabus authorization are grave academic violations. Every assignment submitted must contain a signed Declaration of Originality.

#### Clause 7.2: Sanctions for Plagiarism Infractions
Where a student is determined to have committed academic plagiarism by an Academic Integrity Inquiry Board:
- Level 1 Offense (First offense, textual overlap under 20%): Zero grade awarded for the specific assignment and mandatory completion of an ethical scholarship workshop.
- Level 2 Offense (Substantial plagiarism or unpermitted collaboration): Failing grade 'F' assigned for the entire course, recorded on transcript as disciplinary failure.
- Level 3 Offense (Second major offense, thesis fabrication, or commercial ghost-writing): Immediate suspension from the Institute for a minimum of two (2) semesters or permanent expulsion.

### Section 8: Medical Leaves, Compassionate Absences, and Excuses
#### Clause 8.1: Certified Hospitalization and Attendance Relief [PLANTED CONTRADICTION 1B]
(a) The Institute recognizes that catastrophic illness or sudden surgical emergencies may disrupt continuous classroom participation.
(b) Medical leave is granted solely for inpatient hospitalization in a recognized medical facility or severe contagious illnesses certified by licensed medical doctors.
(c) In case of certified medical hospitalization exceeding five (5) consecutive calendar days, the minimum attendance threshold for end-semester examination eligibility shall be lowered to 65%, provided that official medical certificates and discharge summaries are submitted to and endorsed by the University Health Officer within forty-eight (48) hours of discharge.
(d) Outpatient illnesses, seasonal head colds, voluntary elective procedures, and unverified private physician notes will not be accepted for threshold mitigation under this clause.

#### Clause 8.2: Bereavement Leave
A student who experiences the death of an immediate nuclear family member (parent, legal guardian, sibling, spouse, or child) may be granted up to seven (7) consecutive days of bereavement leave upon submission of a death notice or funeral program to the Dean of Students. Such missed days will be classified as institutional excused absences and excluded from the attendance denominator calculations.

### Section 9: Academic Standing, Probation, and Disqualification
#### Clause 9.1: Good Academic Standing
An undergraduate student maintains Good Academic Standing by preserving a Cumulative Grade Point Average (CGPA) of at least 2.00 on a 4.00 scale and successfully completing at least 67% of attempted cumulative credit hours.

#### Clause 9.2: Academic Warning and Academic Probation
Any student whose semester GPA falls below 2.00 at the end of an academic term will be placed on Academic Probation for the subsequent semester. A student on Academic Probation:
(a) May not register for more than fourteen (14) credit hours during the probationary term.
(b) Is disqualified from participating in intercollegiate varsity athletics or holding executive officer positions in recognized campus student societies.
(c) Must attend weekly peer tutoring and academic counseling sessions coordinated by the Academic Support Center.

#### Clause 9.3: Academic Dismissal
If a student on Academic Probation fails to raise their Cumulative GPA to at least 2.00 after two (2) consecutive semesters on probation, the student will be academically dismissed from the Institute. Dismissed students may lodge a formal reinstatement appeal to the Academic Standing Committee within thirty (30) days of the dismissal notification. Reinstatement is conditional upon completing an academic rehabilitation semester.

### Section 10: Leaves of Absence and Resumption of Studies
#### Clause 10.1: Voluntary Personal and Medical Leaves
A matriculated student in good standing may apply for a temporary Leave of Absence (LOA) for a duration of one (1) or two (2) academic terms. Leaves may be sanctioned for documented medical recuperation, mandatory military or national civil service enlistment, or critical family emergency.

#### Clause 10.2: Leave Duration and Candidature Clock
The cumulative period of sanctioned leaves of absence may not exceed four (4) academic terms during an undergraduate candidature. Time spent on authorized leave of absence does not count against the statutory maximum allowable time to degree completion (six years for a four-year bachelor's degree).

#### Clause 10.3: Resumption of Candidature
To resume studies following a leave of absence, the student must notify the Office of the Registrar in writing at least forty-five (45) calendar days prior to the start of the semester in which they intend to re-enroll. Students returning from medical leave must present a comprehensive medical clearance statement from a licensed physician certifying psychological and physical fitness to resume academic rigor.

### Section 11: Laboratory Safety, Facilities Access, and Capstone Conduct
#### Clause 11.1: General Laboratory Protocols
Safety goggles, fire-retardant lab coats, and closed-toe footwear must be worn at all times inside chemistry, biological engineering, and materials laboratories. No student is permitted to conduct experiments without a certified lab technician or faculty instructor present during standard operating hours. Waste chemicals must be poured into specialized hazardous waste containers and never down municipal drains.

#### Clause 11.2: Research Facility and 24-Hour Computing Lab Privileges [PLANTED CONTRADICTION 2B]
(a) Advanced undergraduate researchers engaged in experimental senior capstone design projects, honors theses, or sponsored departmental research are eligible for extended laboratory access permits.
(b) All enrolled final-year capstone students, honors thesis candidates, and authorized engineering research scholars are granted unhindered twenty-four-hour (24-hour) keycard access to designated campus research laboratories, maker spaces, and the central computing center. Campus security officers, night watchmen, and residential hall wardens are expressly prohibited from impeding, questioning, or locking out students returning to their residence halls from authorized overnight laboratory work sessions, and no fines or disciplinary penalties of any kind shall be levied on such students.
(c) Keys and digital access credentials issued under this clause are non-transferable; loaning access cards to unauthorized persons will incur suspension of laboratory privileges for twelve (12) months.

### Section 12: Undergraduate Capstone Thesis and Graduation Honours
#### Clause 12.1: Bachelor's Thesis Submission Standards
Candidates enrolled in honours programmes must complete an independent research monograph or capstone design thesis consisting of not less than 8,000 words, demonstrating original critical synthesis or empirical laboratory investigation. The capstone thesis must be defended before an examining committee composed of the thesis advisor, one external departmental faculty examiner, and an appointed representative of the Academic Senate.

#### Clause 12.2: Latin Honours and Distinctions
Upon recommendation of the Academic Senate, degrees with Latin honours will be conferred based on final cumulative grade point averages at graduation:
- Summa Cum Laude: Awarded to candidates achieving a cumulative GPA of 3.900 to 4.000 with no recorded disciplinary violations.
- Magna Cum Laude: Awarded to candidates achieving a cumulative GPA of 3.750 to 3.899.
- Cum Laude: Awarded to candidates achieving a cumulative GPA of 3.500 to 3.749.
Honours distinctions are permanently inscribed upon the official parchment diploma and official university transcript.

### Section 13: International Exchange, Transfer Credits, and Summer Sessions
#### Clause 13.1: Study Abroad and Exchange Accreditation
Enrolled undergraduate students who have completed at least sixty (60) credits of study with a CGPA of 3.00 or higher may participate in approved bilateral international exchange programs for up to two (2) semesters. Courses completed at partner universities must receive prior articulation approval from the Department Curriculum Committee. Grades earned abroad appear as Transfer Credit ('TC') and are not factored into the Institute GPA calculation.

#### Clause 13.2: Maximum Transfer Credit Allowances
Undergraduate candidates must complete a minimum of sixty (60) credits in residence at the Apex Institute of Technology & Higher Sciences to qualify for degree conferral. Transfer credits from external universities, advanced placement programs, and international baccalaureate diplomas combined may not exceed sixty (60) total credits toward the 120-credit degree threshold.

#### Clause 13.3: Summer Term Enrollment Limits
During the optional eight-week summer session, students may register for a maximum of eight (8) credits across two modular courses. Summer courses carry identical instructional contact hours, examination formats, and quality points as regular Autumn and Spring semester offerings. Academic probation status continues through the summer term.

### Section 14: Graduation Clearance, Degree Conferral, and Commencements
#### Clause 14.1: Degree Audit Clearance
In the penultimate semester before anticipated graduation, every prospective graduate must file a formal Degree Audit Petition with the Office of the Registrar. The audit verifies completion of general education core courses, departmental major requirements, elective distributions, and minimum cumulative GPA thresholds.

#### Clause 14.2: Financial and Library Clearance
No parchment diploma, official completion letter, or final academic transcript will be released to any graduating student until comprehensive institutional clearance has been granted by the University Library, Student Housing Office, Campus Health Center, and Bursar's Office, verifying zero outstanding debts, unreturned books, or disciplinary fines.
"""

# 2. Hostel and Housing Policy
hostel_policy = """# Apex Institute of Technology & Higher Sciences
## Residential Life Code & Hostel Regulations Handbook

### Section 1: Residential Eligibility, Room Allocation, and Occupancy
#### Clause 1.1: Housing Eligibility and Seniority Tiers
University on-campus accommodation in residential halls and student hostels is available to full-time matriculated students registered for at least twelve (12) credits in the active semester. Room assignments are prioritized on a tiered seniority basis: first-year freshmen receive guaranteed housing allocations, followed by student residential advisors, international exchange candidates, and upperclassmen sorted by cumulative academic grade point average. Part-time students or students on disciplinary probation are ineligible for on-campus dormitory residence.

#### Clause 1.2: Room Inventory and Condition Check-In
Upon receiving room keys, each resident must conduct an exhaustive condition inventory audit utilizing the digital housing mobile app within forty-eight (48) hours of arrival. Any pre-existing structural damage, defective electrical fittings, scratched desks, or broken window screens must be documented with timestamped photographs. Failure to submit the audit report within forty-eight hours establishes conclusive presumption that the room and all inventory were transferred in flawless condition, and the resident will be held financially liable for any defects discovered upon move-out.

#### Clause 1.3: Security Deposits and Move-Out Deductions
A refundable housing damage security deposit of $300 is charged at the commencement of each residential lease. Upon move-out inspection at the end of the academic year, costs incurred for deep cleaning, repainting damaged plaster, repairing broken furniture, or replacing unreturned brass keys will be deducted directly from this deposit. Remaining funds are remitted via electronic bank transfer within thirty (30) business days. In cases where repair costs exceed $300, an administrative charge will be posted to the student's central financial ledger.

### Section 2: Residential Conduct, Quiet Hours, and Community Standards
#### Clause 2.1: Quiet Hours and Noise Mitigation
To foster an environment conducive to scholarly pursuit and restorative sleep, mandatory Quiet Hours are enforced across all hostel premises, residential courtyards, and communal corridors:
- Sunday through Thursday: 23:00 (11:00 PM) to 07:00 (7:00 AM).
- Friday and Saturday: 00:00 (Midnight) to 08:00 (8:00 AM).
During Quiet Hours, sound from stereos, televisions, musical instruments, vocal conversations, and gaming consoles must not be audible beyond the closed doorway of any residential unit. Courtesy Hours are in effect twenty-four hours a day; residents must lower volume immediately upon polite request by another resident or hostel steward. Repetitive noise complaints will trigger referral to the Hall Disciplinary Committee.

#### Clause 2.2: Guest Regulations and Overnight Visitors
Daytime guests are permitted inside hostel common lounges between 08:00 and 21:30 daily. All non-resident guests must present government photo identification and sign the register at the security desk upon arrival. Overnight visitors are permitted for a maximum of two (2) consecutive nights and no more than four (4) nights per calendar month, subject to advance written consent signed by all room occupants and verified by the Hall Warden at least twenty-four (24) hours before guest arrival. Underage guests under eighteen (18) years of age are not permitted overnight accommodations under any circumstance.

#### Clause 2.3: Cohabitation and Unauthorized Subletting
Subletting, transferring room leases, exchanging bed assignments without administrative approval, or permitting unauthorized continuous cohabitation is strictly prohibited. Violations will result in immediate termination of the housing license agreement, forfeiture of the damage deposit, and disciplinary referral to the Proctorial Board. Residents who knowingly harbor unauthorized subletters face permanent bans from on-campus housing.

### Section 3: Curfew Protocols, Late Entry Sanctions, and Access Control
#### Clause 3.1: Perimeter Security and Keycard Entry
Hostel exterior perimeter gates and entrance vestibules are secured with RFID biometric electronic keycards twenty-four hours a day. Residents must swipe their personal keycard individually; "tailgating" or holding exterior doors open for unrecognized individuals is a security hazard subject to formal warning. Security cameras continuously monitor all entry and exit turnstiles.

#### Clause 3.2: Overnight Absences and Sign-Out Slips
Any resident planning to spend the night away from their assigned hostel (at a family home, weekend excursion, or private lodging) must complete the overnight leave register located at the reception lodge prior to 20:00 on the day of departure, recording emergency contact details and expected return date. Failure to record overnight absences compromises fire evacuation roll calls and results in a formal written notice to the resident's emergency contact.

#### Clause 3.3: Lost Keys and Lockout Fees
Residents who lock themselves out of their rooms may request lock-out assistance from the resident tutor on duty. The initial lock-out assistance in an academic term is performed without fee; subsequent lock-out requests incur a $15 administrative service fee billed to the student's term account. Lost electronic access badges incur a replacement fee of $35. Duplicate keys may not be made at private locksmith establishments.

#### Clause 3.4: Mandatory 22:00 Curfew and Strict Gate Penalties [PLANTED CONTRADICTION 2A]
A mandatory residential gate curfew is strictly enforced across all undergraduate hostels at 22:00 (10:00 PM) daily. Any resident entering the residential precinct or dormitory block after 22:00 without a physical, pre-authorized written warden leave slip signed before 17:00 of the same day shall incur a mandatory fine of $50 and shall be locked out of the hostel until 06:00 the following morning. Security wardens have zero discretion to waive this lock-out.

### Section 4: Prohibited Substances, Health, and Safety Regulations
#### Clause 4.1: Smoke-Free and Substance-Free Environment
All hostel buildings, individual bedrooms, balconies, communal kitchens, stairwells, and outdoor grounds within fifty (50) feet of residential perimeters are designated strictly non-smoking and tobacco-free zones. This ban encompasses traditional cigarettes, electronic cigarettes, vaping apparatuses, hookahs, and heated tobacco products. Possession or consumption of alcoholic beverages by underage students, or possession of any illicit scheduled narcotics, will result in instant eviction from campus housing and immediate referral to municipal police authorities.

#### Clause 4.2: Fire Prevention and Combustible Materials
Open flames, candles, incense burners, oil lamps, fireworks, kerosene heaters, propane stoves, lighter fluid, gasoline, and combustible compressed gas canisters are strictly forbidden inside residential buildings. Tampering with fire extinguishers, smoke detectors, emergency sprinkler heads, or triggering malicious false fire alarms carries a non-negotiable fine of $250 plus repair costs and potential criminal prosecution.

#### Clause 4.3: Electrical Appliance Restrictions
To avert electrical circuit overloads and fire hazards, high-draw electrical heating appliances are strictly banned from student bedrooms. Banned items include immersion water heaters, induction cooktops, hot plates, portable space heaters, electric frying pans, toaster ovens, and electric deep fryers. Approved appliances are limited to electric kettles with automatic shut-off switches (not exceeding 1000 watts), hair dryers (under 1500 watts), desk lamps, laptop power bricks, and mobile phone chargers. Unauthorized appliances will be impounded until move-out.

### Section 5: Room Sanitation, Inspections, and Maintenance
#### Clause 5.1: Health and Hygiene Routine Inspections
Residential staff and facilities management inspectors conduct monthly scheduled health, hygiene, and electrical safety inspections. Residents will be given at least twenty-four (24) hours advance digital notification before routine entries. Rooms must be maintained in a clean, hygienic state free of decaying perishable food, mold buildup, overflowing trash receptacles, and severe pest attractants.

#### Clause 5.2: Animal and Pet Prohibition
To protect community health, prevent allergic reactions, and preserve facility sanitation, no live animals, domesticated pets, birds, reptiles, or stray animals may be brought into, kept, or sheltered in any hostel building or room. Certified guide dogs assisting registered visually impaired students are the sole exception, subject to prior filing with the Campus Disability Office and Hall Warden.

#### Clause 5.3: Waste Disposal and Recycling
Residents must deposit domestic garbage and recyclables into designated segregated waste bins located in central utility alcoves on each floor. Leaving garbage bags in hallway corridors, staircases, or communal bathroom lobbies constitutes a sanitation violation subject to a $20 cleanup levy per incident.

### Section 6: Room Reassignments, Cancellations, and Vacating Protocols
#### Clause 6.1: Administrative Room Reassignments
The Housing Office reserves the right to consolidate vacancies or reassign students to alternative residential quarters when occupancy in a wing drops below 50%, or where urgent structural maintenance, plumbing remediation, or safety emergencies necessitate building evacuation.

#### Clause 6.2: Room Transfer Requests
Residents wishing to swap rooms or transfer to a different residential hall must submit a formal Room Transfer Request during the third week of the academic term. Transfers are contingent upon mutual consent between swapping parties, absence of disciplinary proceedings, and payment of a $50 room transfer processing fee. Room transfers are not authorized on grounds of trivial personality friction until residents have completed a mediation conference facilitated by their Resident Advisor.

#### Clause 6.3: Mid-Semester Housing Cancellation
A resident who vacates campus housing prior to the completion of the contractual term without withdrawing from the university remains liable for 100% of the semester housing rent, unless the student can demonstrate extreme unforeseen medical or financial calamity verified by the Dean of Students.

### Section 7: Dining Halls, Meal Plans, and Food Safety
#### Clause 7.1: Compulsory Meal Plans for First-Year Residents
All first-year residential students residing in traditional dormitory halls are required to participate in the University Dining Plan (Tier A or Tier B). Tier A provides nineteen (19) dining hall meals per week; Tier B provides fourteen (14) meals per week along with $200 in flex dining credits redeemable at campus cafes.

#### Clause 7.2: Dining Hall Conduct and Removal of Food
Food prepared within the dining commons must be consumed within the dining facility. Removing bulk food, chafing dish pans, crockery, cutlery, or stainless steel serving utensils from the dining hall is strictly prohibited and constitutes residential theft. Students may remove one piece of fresh hand fruit or one bakery cookie upon exit.

#### Clause 7.3: Communal Kitchen Etiquette
Upperclass halls equipped with shared floor kitchens provide electric induction stoves, shared refrigerators, and microwave ovens. Residents using communal kitchens must wash, dry, and store their cookware immediately following meal preparation. Unlabeled food left in communal refrigerators for more than seven (7) days will be discarded without notice during weekly sanitation sweeps.

### Section 8: Communal Laundry Facilities, Package Mailrooms, and Storage
#### Clause 8.1: Laundry Facility Usage
Each residential block is equipped with automated washing machines and tumble dryers operated via student smart-card credits. Residents must remove cleaned clothes promptly upon completion of wash and dry cycles. Abandoned clothing left in laundry hampers for over forty-eight (48) hours will be donated to local charitable clothing drives.

#### Clause 8.2: Mailroom Package Delivery and Identification
Personal parcels and courier deliveries are received at the Central Campus Mailroom. Residents receive an automated electronic SMS pickup notification when a parcel is logged. Packages must be collected within ten (10) business days upon presenting an official student photo identification card; unclaimed parcels are returned to the sender.
"""

# 3. Scholarship and Financial Aid Policy
scholarship_policy = """# Apex Institute of Technology & Higher Sciences
## Institutional Scholarships, Bursaries, and Financial Aid Guidelines

### Section 1: Merit-Based Academic Scholarships
#### Clause 1.1: Chancellor's Premier Academic Scholars Award
The Chancellor's Premier Academic Scholars Award is the Institute's most prestigious merit endowment, awarded to incoming first-year undergraduate students who placed within the top 0.5 percentile of national matriculation examinations. The scholarship provides:
(a) Full coverage of all standard semester tuition fees for eight (8) consecutive academic terms.
(b) Exemption from mandatory campus laboratory and computer technology fees.
(c) A semesterly living stipend of $1,500 deposited directly into the recipient's institutional bank account.
(d) Priority allocation of single-occupancy on-campus residential accommodation.

#### Clause 1.2: Academic Excellence Continuing Student Scholarships
Continuing undergraduate students who completed at least thirty (30) credit hours at the Institute and achieved a Cumulative Grade Point Average (CGPA) of 3.85 or higher over the preceding academic year are eligible to receive the Dean's Academic Excellence Scholarship. This award grants a 50% tuition reduction for the subsequent two regular semesters. Awards are competitive and capped at the top five percent (5%) of students within each academic faculty.

#### Clause 1.3: Maintenance of Merit Scholarship Eligibility
Recipients of merit-based awards must satisfy continuous performance standards to maintain scholarship benefits:
(a) The student must maintain a minimum Cumulative GPA of 3.75 evaluated at the conclusion of each Spring term.
(b) The student must successfully complete a minimum of fifteen (15) academic credits per regular semester.
(c) The recipient must have no recorded findings of academic dishonesty or code of conduct infractions on their disciplinary record.

#### Clause 1.4: Scholarship Probation and Reinstatement
If a merit scholarship recipient's CGPA dips below 3.75 but remains at or above 3.50 at the annual review, the student is placed on Scholarship Probation for one (1) semester. During the probationary term, financial aid disbursements remain active. If the student elevates their CGPA to 3.75 or above by the end of the probationary semester, full scholarship standing is restored. If the CGPA remains below 3.75, the scholarship is permanently revoked.

### Section 2: Need-Based Bursaries and Emergency Assistance
#### Clause 2.1: Campus Opportunity Access Bursary
The Campus Opportunity Access Bursary provides grant assistance to matriculated students from socio-economically disadvantaged backgrounds. Eligibility is evaluated through documented parental income tax filings, household asset appraisals, and verified dependents. Bursary awards range from 25% to 100% tuition remission and do not require repayment. Applications must be resubmitted annually during the priority filing window (March 1 to April 30).

#### Clause 2.2: Hardship Emergency Aid Fund
The Dean of Students administers the Emergency Student Relief Fund, which offers one-time emergency micro-grants up to $1,000 for enrolled students facing acute, unexpected financial catastrophes (such as sudden family breadwinner death, house fires, or uninsured medical crises). Emergency grants are limited to one distribution per student per degree programme and cannot be utilized to liquidate past-due tuition balances from prior terms.

### Section 3: Work-Study Programme and Student Employment
#### Clause 3.1: Work-Study Positions and Allocation
Eligible financial aid recipients may be placed in campus work-study assignments across academic department offices, library reference desks, computing labs, and dining halls. Work-study wages are disbursed bi-weekly at the regional minimum wage plus a $1.50 per hour institutional supplement.

#### Clause 3.2: Maximum Work Hours During Instructional Terms
To ensure student employment does not impair academic achievement, students enrolled in full-time courses are prohibited from working more than fifteen (15) cumulative hours per week in campus employment during active instructional weeks. During scheduled university vacations (summer recess and winter intersession), work hours may be expanded up to thirty-five (35) hours per week with department approval.

### Section 4: External Awards and Stacking Policies
#### Clause 4.1: Reporting of External Sponsorships
All students receiving outside corporate sponsorships, civic foundation grants, or foreign government educational allowances must report such awards to the Financial Aid Office within ten (10) days of receipt.

#### Clause 4.2: Institutional Award Stacking Limits
The total aggregate value of all institutional scholarships, departmental grants, and external fee allowances received by a student may not exceed the total cost of attendance (encompassing tuition, mandatory campus fees, room, and board) for that academic year. If the aggregate sum exceeds the cost of attendance, the Institute's institutional aid will be reduced proportionally to eliminate the excess surplus.

### Section 5: Athletic Grants and Extracurricular Endowments
#### Clause 5.1: Varsity Athletic Performance Scholarships
Student athletes competing on official intercollegiate varsity sports teams may receive athletic grants awarded upon recommendation of the Director of Intercollegiate Athletics. Recipients must participate in all scheduled practices, maintain full-time academic enrollment, and preserve a minimum CGPA of 2.50.

#### Clause 5.2: Injury and Scholarship Continuity
A student athlete who incurs a season-ending or career-terminating athletic injury while representing the Institute in sanctioned intercollegiate competition will retain their athletic scholarship funding for the remainder of their standard four-year undergraduate programme, provided they maintain good academic standing and serve as an athletic mentor or team statistician.
"""

# 4. Fee Deadlines and Refunds Schedule (CSV format)
csv_content = [
    ["Transaction_Category", "Deadline_or_Window", "Financial_Penalty_or_Refund_Tier", "Governing_Policy_Terms"],
    ["Semester Tuition Payment", "Day 0 (Prior to First Day of Class)", "Full Balance Due (0% penalty)", "Standard registration clearance. Registration canceled if unpaid by 17:00."],
    ["Late Registration Fee", "Day 1 to Day 7 of Semester", "$50 Fixed Late Surcharge", "Permitted only if seats remain available in enrolled courses."],
    ["Extended Late Registration", "Day 8 to Day 14 of Semester", "$100 Escalated Late Surcharge", "Requires written authorization from the Dean of Academic Affairs."],
    ["Course Withdrawal (Day 15 to Day 35)", "Day 15 to Day 35 of Semester", "0% Refund (100% Tuition Forfeiture)", "Strict forfeiture policy [PLANTED CONTRADICTION 3B]. No tuition refunds, rebates, or credits shall be issued for course drops or withdrawals recorded between Day 15 and Day 35 of the academic semester."],
    ["Complete University Term Withdrawal", "Prior to Day 7 of Semester", "100% Tuition Refund minus $100 Admin Fee", "Formal withdrawal from all courses processed through Registry."],
    ["Complete University Term Withdrawal", "Day 8 to Day 14 of Semester", "75% Tuition Refund", "Prorated refund credited to source account within 21 banking days."],
    ["Complete University Term Withdrawal", "Day 15 to Day 28 of Semester", "50% Tuition Refund", "Half tuition forfeited; laboratory and tech fees non-refundable."],
    ["Complete University Term Withdrawal", "After Day 28 of Semester", "0% Refund (100% Total Forfeiture)", "Full liability for semester tuition, campus fees, and laboratory levies."],
    ["Hostel Rent Cancellation", "Before Housing Move-in Date", "90% Rent Refund", "10% processing fee retained by Housing Office."],
    ["Hostel Rent Cancellation", "Day 1 to Day 14 after Move-in", "50% Rent Refund", "Damage deposit refunded after mandatory room inspection."],
    ["Hostel Rent Cancellation", "After Day 14 of Occupancy", "0% Rent Refund", "Resident remains liable for full semester housing rent."],
    ["Graduation & Commencement Fee", "Due by Week 10 of Final Semester", "$150 Mandatory Fee", "Covers cap and gown rental, diploma parchment, and degree audit."],
    ["Official Transcript Request", "Standard 5-day Processing", "$15 Per Copy", "Electronic PDF or stamped paper parchment dispatched by postal mail."],
    ["Express Transcript Request", "Same-day 24-hour Processing", "$35 Per Copy", "Expedited courier delivery dispatched same day."],
    ["Library Overdue Book Fine", "1 to 14 Days Overdue", "$1.00 Per Day Per Volume", "Borrowing privileges suspended until overdue items returned."],
    ["Library Lost Book Replacement", "Exceeding 30 Days Overdue", "Cost of Book + $40 Processing Fee", "Standard catalog replacement pricing applied."],
    ["Hostel Room Lockout Service", "First occurrence per term: Free", "$15 Per Subsequent Occurrence", "Billed to student term account by Residential Life Office."],
    ["Hostel Lost Electronic Keycard", "Immediate replacement", "$35 Administrative Surcharge", "Old keycard electronically deactivated instantly across all turnstiles."]
]

# 5. Disciplinary Charter and Standing Orders (PDF)
disciplinary_text = """
Apex Institute of Technology & Higher Sciences
Standing Charter of the Proctorial Board and Senate Committees (Volume IX)

Section 1: Jurisdictional Foundations and Proctorial Powers
Clause 1.1: Establishment of the Proctorial Board
The Proctorial Board is constituted by the Board of Governors as the primary investigative and disciplinary authority for non-academic misconduct. The Board exercises campus-wide jurisdiction over student behavior in university precincts, student halls of residence, digital institutional networks, and official off-campus field excursions.

Clause 1.2: Investigative Authorities and Summons
The Chief Proctor and designated Deputy Proctors are empowered to issue formal summons, interview witnesses, subpoena campus security footage, inspect digital network logs, and conduct evidentiary hearings regarding allegations of misconduct. Any student who fails to appear before a proctorial summons without verified medical incapacitation shall be subject to immediate interim suspension.

Clause 1.3: Summary Jurisdiction for Minor Infractions
Deputy Proctors may exercise summary jurisdiction over minor behavioral infractions occurring within their geographical zones, including smoking violations, minor property noise nuisance, and unauthorized parking. Summary penalties are capped at a $100 fine or twenty (20) hours of supervised campus community service.

Section 2: Disciplinary Hearings and Student Rights
Clause 2.1: Principles of Natural Justice
Every student charged with a disciplinary violation is guaranteed the fundamental protections of natural justice:
(a) The right to receive a written Statement of Charges specifying alleged violations at least five (5) working days prior to any formal hearing.
(b) The right to review all documentary and video evidence assembled by the Proctorial Office.
(c) The right to present oral testimony, submit witness statements, and introduce exculpatory material.
(d) The right to be accompanied by a student peer advisor or member of the campus student legal clinic (formal external legal counsel is not permitted to plead before the internal board).

Clause 2.2: Standard of Proof
The standard of proof applied in all proctorial and senate disciplinary hearings is the preponderance of probabilities; the board determines whether it is more likely than not that the contested incident occurred.

Section 3: Disciplinary Sanction Hierarchy
Clause 3.1: Authorized Penalties and Sanctions
Upon a formal determination of misconduct, the Proctorial Board may impose one or more of the following sanctions:
(a) Formal Written Reprimand placed in the student's confidential registry file.
(b) Disciplinary Restitution and monetary fines to compensate for physical damage to university property.
(c) Restriction of Campus Privileges (including bar on vehicle registration, removal from student societies, or exclusion from licensed social facilities).
(d) Residential Hall Eviction (permanent or temporary removal from on-campus housing).
(e) Disciplinary Suspension from the Institute for a period spanning from one semester to two full academic years.
(f) Permanent Expulsion with irrevocable forfeiture of matriculation standing.

Section 4: Standing Powers of the Academic Standing & Petitions Committee
Clause 14.1: Authority and Composition
The Academic Standing & Petitions Committee is a statutory committee of the Academic Senate, chaired by the Vice-Provost for Academic Affairs and comprising five tenured department chairs and two elected student senate representatives.

Clause 14.2: General Waiver Authority
The Committee is invested with executive discretion to evaluate extraordinary hardship petitions regarding degree completion hurdles, retroactive term withdrawals, and curriculum substitution requests where strict application of standard statutes would produce grave injustice.

Clause 14.3: Special Jurisdiction on Examination Attendance Dispensations [PLANTED CONTRADICTION 1C]
The Academic Standing & Petitions Committee possesses sole, plenary, and unappealable jurisdiction to grant examination sitting dispensations to any enrolled matriculated student whose course attendance stands between 50.0% and 74.9%, upon formal petition submitted to the Committee at least seven (7) calendar days prior to the commencement of the examination period. The Committee may mandate alternative remedial assessments, capstone essays, or oral vivas in lieu of standard physical attendance contact hours. Decisions rendered under this clause are final and binding across all academic faculties.

Section 5: Appeals Procedure and Appellate Senate Standing Board
Clause 18.1: Grounds for Formal Appeal
A student subjected to suspension, expulsion, or significant financial sanction may lodge an appeal to the Appellate Senate Standing Board within fourteen (14) calendar days of receiving written notice of sanction. Appeals are limited strictly to three legal grounds:
(a) Procedural irregularity substantial enough to have prejudiced the hearing outcome.
(b) Emergence of new material evidence that was genuinely unavailable at the time of the original inquiry.
(c) Gross disproportion of the sanction relative to the severity of the established infraction.

Clause 18.2: Appellate Rulings and Finality
The Appellate Senate Standing Board reviews the transcribed hearing records and submissions. The Board may affirm the original penalty, reduce the severity of the sanction, or order a de novo re-hearing before an alternate panel. Rulings of the Appellate Board are final and unappealable within the Institute.

Section 6: Record Retention, Expungement, and Restorative Measures
Clause 22.1: Disciplinary Record Retention
Records of disciplinary admonitions and minor fines are maintained confidentially in the Office of the Proctor for a duration of five (5) years following the student's graduation, after which they are systematically purged. Records of suspensions and expulsions remain a permanent part of the archival institutional record.

Clause 22.2: Petition for Disciplinary Record Expungement
A student who received a single Level 1 disciplinary sanction may petition the Proctorial Board for record expungement during their final semester of study, provided the student has completed twenty-five (25) hours of certified campus service and sustained no further disciplinary complaints.
"""

def generate_pdf(filename, text_content):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=14
    )
    
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=12,
        spaceAfter=8
    )
    
    h3_style = ParagraphStyle(
        'DocH3',
        parent=styles['Heading3'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#2d3748'),
        spaceBefore=8,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1a202c'),
        spaceAfter=6
    )

    story = []
    lines = text_content.strip().split('\n')
    for line in lines:
        line_s = line.strip()
        if not line_s:
            story.append(Spacer(1, 4))
            continue
        if line_s.startswith("Apex Institute") or line_s.startswith("Standing Charter"):
            story.append(Paragraph(line_s, title_style))
        elif line_s.startswith("Section "):
            story.append(Paragraph(line_s, h2_style))
        elif line_s.startswith("Clause "):
            story.append(Paragraph(line_s, h3_style))
        else:
            story.append(Paragraph(line_s, body_style))

    doc.build(story)

def main():
    # Write Markdown files
    with open(os.path.join(CORPUS_DIR, "academic_regulations.md"), "w", encoding="utf-8") as f:
        f.write(academic_regulations)
    
    with open(os.path.join(CORPUS_DIR, "hostel_and_housing_policy.md"), "w", encoding="utf-8") as f:
        f.write(hostel_policy)
        
    with open(os.path.join(CORPUS_DIR, "scholarship_and_aid_policy.md"), "w", encoding="utf-8") as f:
        f.write(scholarship_policy)

    # Write CSV
    with open(os.path.join(CORPUS_DIR, "fee_deadlines_and_refunds.csv"), "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(csv_content)

    # Generate PDF
    pdf_path = os.path.join(CORPUS_DIR, "disciplinary_charter.pdf")
    generate_pdf(pdf_path, disciplinary_text)

    # Word count tally
    words_acad = len(academic_regulations.split())
    words_hostel = len(hostel_policy.split())
    words_schol = len(scholarship_policy.split())
    words_csv = sum(len(" ".join(row).split()) for row in csv_content)
    words_pdf = len(disciplinary_text.split())
    total_words = words_acad + words_hostel + words_schol + words_csv + words_pdf

    print(f"Corpus Generation Complete:")
    print(f" - academic_regulations.md: {words_acad} words")
    print(f" - hostel_and_housing_policy.md: {words_hostel} words")
    print(f" - scholarship_and_aid_policy.md: {words_schol} words")
    print(f" - fee_deadlines_and_refunds.csv: {words_csv} words")
    print(f" - disciplinary_charter.pdf: {words_pdf} words")
    print(f"TOTAL WORD COUNT: {total_words} words (Requirement: >= 6,000 words)")

if __name__ == "__main__":
    main()
