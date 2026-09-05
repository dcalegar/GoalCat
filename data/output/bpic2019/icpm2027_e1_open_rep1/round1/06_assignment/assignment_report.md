# Step 6 — Narrative assignment report

Run: `icpm2027_e1_open_rep1` | Log: `bpic2019` | Taxonomy mode: `open` | Assignment model: `gemini/gemini-3.5-flash-lite`

11973 variants, 251734 cases total.

## Standard Procurement Flow (`standard_procurement_flow`)

Standard purchasing and invoicing paths with predictable sequences, moderate lead times, and clean execution.

**Taxonomy-derivation rationale (Step 5):** Represents the most frequent baseline purchasing processes (e.g. V0001, V0002) which lack extreme durations or rework anomalies.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 4782/11973 variants (39.9%) · micro 197642/251734 cases (78.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 7.10, nearest other category `srm_integration_anomaly` at mean distance 14.16

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.413, nearest other category `extreme_duration_and_churn` at mean distance 0.433

## Short/Low-Touch Flow (`short_low_touch_flow`)

Short trace lengths consisting of early-stage procurement actions, rapid deletions, or immediate creation/goods receipt actions without full invoicing loops.

**Taxonomy-derivation rationale (Step 5):** Captures low-length traces like simple order creations, deletions, or quick receipts (e.g. V0003, V0009, V0014, V0024) with minimal operational footprint.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 951/11973 variants (7.9%) · micro 36526/251734 cases (14.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 35.31, nearest other category `standard_procurement_flow` at mean distance 25.36

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.538, nearest other category `service_entry_and_rework` at mean distance 0.547

## Service Entry & Minor Rework (`service_entry_and_rework`)

Flows centered around service entry sheets with minor repetitions or immediate low-duration completions.

**Taxonomy-derivation rationale (Step 5):** Reflects execution patterns featuring service entry and goods receipt loops or small repetitions without exploding into massive delays (e.g. V0064, V0162, V0244, V0271).

**Goal-model linkage:** (no goal model)

**Coverage:** macro 2797/11973 variants (23.4%) · micro 7690/251734 cases (3.1%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 82.46, nearest other category `standard_procurement_flow` at mean distance 62.74

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.426, nearest other category `short_low_touch_flow` at mean distance 0.547

## SRM Integration Anomaly (`srm_integration_anomaly`)

Flows involving SRM sub-system milestones, transfers, transmission changes, or system transfer failures.

**Taxonomy-derivation rationale (Step 5):** Isolates complex variants tied to SRM tracking states and transfer errors (e.g. V2944, V2952, V2950, V2949, V2947, V2946, V2948) which exhibit specialized messaging.

**Goal-model linkage:** (no goal model)

**Coverage:** macro 194/11973 variants (1.6%) · micro 1284/251734 cases (0.5%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 10.98, nearest other category `standard_procurement_flow` at mean distance 14.16

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.513, nearest other category `standard_procurement_flow` at mean distance 0.523

## Extreme Duration and Churn (`extreme_duration_and_churn`)

Massive trace lengths, extensive document cancellations, repetitive invoice postings, and multi-year durations.

**Taxonomy-derivation rationale (Step 5):** Captures extreme outliers characterized by hundreds of activities, pervasive churn, invoice cancellations, and massive wait times spanning thousands of days (e.g. V1038, V3680, V3305, V3102, V3074, V6776, V5418).

**Goal-model linkage:** (no goal model)

**Coverage:** macro 2969/11973 variants (24.8%) · micro 5818/251734 cases (2.3%)

**Cohesion — structural (control-flow proximity):** intra-category mean distance 35.60, nearest other category `standard_procurement_flow` at mean distance 23.10

**Cohesion — profile (duration/outcome/rework):** intra-category mean distance 0.392, nearest other category `standard_procurement_flow` at mean distance 0.433

## Divergence between structural and profile distance

Flagged for review, not resolved automatically — the two metrics measure different things (control-flow vs. business profile) and disagreement is informative on its own.

**Same category, structurally far apart** (possibly a category covering two distinct control-flow patterns):

- `V1618` / `V6776` (category `extreme_duration_and_churn`): structural=989, profile=0.723
- `V2258` / `V6776` (category `extreme_duration_and_churn`): structural=989, profile=0.726
- `V2259` / `V6776` (category `extreme_duration_and_churn`): structural=989, profile=0.726
- `V2937` / `V6776` (category `extreme_duration_and_churn`): structural=989, profile=0.725
- `V4364` / `V6776` (category `extreme_duration_and_churn`): structural=989, profile=0.730
- `V5367` / `V6776` (category `extreme_duration_and_churn`): structural=989, profile=0.726
- `V5368` / `V6776` (category `extreme_duration_and_churn`): structural=989, profile=0.726
- `V5457` / `V6776` (category `extreme_duration_and_churn`): structural=989, profile=0.720
- `V6113` / `V6776` (category `extreme_duration_and_churn`): structural=989, profile=0.729
- `V6776` / `V6903` (category `extreme_duration_and_churn`): structural=989, profile=0.739

**Different category, structurally near-identical** (the TP/TA-style case — categories distinguished on business intent the activity sequence alone would not show):

- `V0001` (`standard_procurement_flow`) / `V0192` (`extreme_duration_and_churn`): structural=1, profile=0.686
- `V0001` (`standard_procurement_flow`) / `V0383` (`service_entry_and_rework`): structural=1, profile=0.003
- `V0001` (`standard_procurement_flow`) / `V0564` (`short_low_touch_flow`): structural=1, profile=0.334
- `V0001` (`standard_procurement_flow`) / `V1235` (`service_entry_and_rework`): structural=1, profile=0.006
- `V0001` (`standard_procurement_flow`) / `V1652` (`service_entry_and_rework`): structural=1, profile=0.684
- `V0001` (`standard_procurement_flow`) / `V7341` (`service_entry_and_rework`): structural=1, profile=0.335
- `V0001` (`standard_procurement_flow`) / `V11593` (`short_low_touch_flow`): structural=1, profile=0.345
- `V0001` (`standard_procurement_flow`) / `V11917` (`short_low_touch_flow`): structural=1, profile=0.034
- `V0002` (`standard_procurement_flow`) / `V0062` (`service_entry_and_rework`): structural=1, profile=0.002
- `V0002` (`standard_procurement_flow`) / `V0096` (`service_entry_and_rework`): structural=1, profile=0.334

## Residual

280/11973 variants (2.3%), 2774/251734 cases (1.1%) unassigned.

- `V0027`: The flow is prolonged and anomalous without completing a standard end-to-end clearing loop, remaining residual.
- `V0079`: Involves cancellations and debit memos over a prolonged duration that do not fit standard flows or other specific categories.
- `V0088`: Characterized by cancellations and debit memos rather than a standard or low-touch flow.
- `V0091`: Involves cancellations of goods and invoice receipts over an extended duration without completing a standard flow.
- `V0121`: Does not fit standard flows due to long duration and ending in a purchase order block, but lacks the extreme churn of extreme duration categories.
- `V0130`: Repetitive purchase order approvals that do not fit standard purchasing, low-touch paths, SRM, or extreme duration patterns.
- `V0257`: Trace consists primarily of cancellations and a debit memo without a full standard procurement loop.
- `V0279`: Trace ends at record invoice receipt without standard completion, but does not fit extreme churn or SRM patterns.
- `V0329`: Starts with debit memo and involves cancellations and price changes out of standard sequential order, falling into the residual flow.
- `V0337`: Involves cancellations of goods and invoice receipts driven by a debit memo, representing a non-standard exception path.
- `V0347`: Contains complex cancellations and repeated clearing loops that do not cleanly match standard paths or extreme churn definitions.
- `V0350`: Consists primarily of repeated approval changes on purchase orders, falling outside the standard procurement or service flow definitions.
- `V0357`: Features debit memos and cancellations which do not cleanly fit standard flows or other categories.
- `V0367`: Unusual late cancellation of invoice receipt after a long duration, not fitting standard categories.
- `V0384`: Does not clearly map to any specific category; involves repeated goods receipt without full invoicing or typical service entry characteristics.
- `V0386`: Involves invoice receipt repetition and longer duration, but does not fit cleanly into standard flows or extreme churn.
- `V0390`: Repeated goods receipt without matching service entry or other clean categories.
- `V0391`: Features multiple repetitions of goods receipts and invoice receipts, not fitting neatly into standard single-flow categories.
- `V0394`: Terminates in cancel invoice receipt with an extended duration, not matching standard clean flows.
- `V0395`: Involves duplicated invoice receipts and payment blocks.
- `V0399`: Involves cancellations and delivery indicator changes, fitting none of the primary categories.
- `V0550`: An inverted chronological sequence starting with a change approval and vendor invoice before PO creation, fitting none of the standard patterns.
- `V0624`: Does not fit standard or low-touch categories; features chaotic sequence of approvals and does not clearly align with standard definitions.
- `V0758`: Does not fit any category cleanly due to late goods receipt occurring after invoice clearing.
- `V0926`: This flow features multiple invoice cancellations and repeated invoice clearings, placing it outside of standard or clean execution.
- `V0927`: The process contains payment blocks, debit memos, and invoice cancellation loops which do not align with any primary category.
- `V0929`: Involves multiple invoice receipts, debit memos, payment blocks, and cancellations, indicating a complex rework loop.
- `V0930`: Repeated goods receipts, invoice receipts, and multiple invoice creations create a high-churn path.
- `V0931`: Contains duplicate invoice receipts and multiple iterations that go beyond standard flows.
- `V0932`: Centered on repeated goods receipts and ending in a goods receipt cancellation.
- `V0934`: Features multiple changes to approval, price, and quantity along with invoice cancellations and repetition.
- `V0936`: Heavy repetition of goods receipt events characterizes this anomaly.
- `V0938`: Features extensive repetition of goods receipt actions before proceeding to invoice receipt.
- `V0940`: Complex sequence involving debit memos, invoice cancellations, and repeated clearings.
- `V0941`: Ends in an invoice receipt cancellation after a multi-step procurement and invoicing path.
- `V0942`: Terminates with a delayed invoice receipt cancellation.
- `V0943`: Exhibits duplicated goods receipts, invoice creations, and invoice receipts.
- `V0944`: Contains duplicated invoice creations and repeated invoice receipts.
- `V0947`: Characterized by multiple price and quantity change cycles before reaching final processing.
- `V0948`: Features invoice cancellations, repeated clearings, and multiple invoice receipts.
- `V0949`: Includes goods receipt cancellation and repetition before payment block removal.
- `V0950`: High degree of repetition in invoices, goods receipts, invoice receipts, and clearings.
- `V1004`: Involves invoice cancellations and debit memos which go beyond standard flows, but does not cleanly fit extreme duration or SRM anomaly patterns.
- `V1005`: Contains multiple repeated invoice postings, payment block removals, and invoice cancellations creating extensive churn outside standard flow descriptions.
- `V1008`: Features repeated goods receipts and invoice receipts with moderate duration, falling into residual due to rework complexity.
- `V1015`: Involves multiple repetitions of goods receipts, invoices, and clearing steps causing rework churn.
- `V1017`: Involves invoice cancellations, debit memos, and long durations spanning multiple months.
- `V1018`: Features debit memos, quantity changes, and invoice cancellations spanning several months.
- `V1019`: Contains duplicate invoicing and goods receipt loops requiring payment block removal.
- `V1022`: Involves quantity changes and duplicate invoice receipts leading to moderate churn.
- `V1023`: Contains goods receipt cancellations and payment block removals.
- `V1025`: Involves item deletion and repeated purchase order approvals that do not fit standard purchasing flows.
- `V1064`: Does not clearly fit any standard category due to prolonged waiting time ending prematurely at invoice receipt without full payment clearing or extreme churn.
- `V1101`: This variant involves a purchase order item deletion following a goods receipt cancellation, which does not cleanly fit standard flows, service entries, or extreme churn patterns.
- `V1102`: The narrative features a cancellation of a subsequent invoice and payment block adjustments, falling outside the standard procurement or low-touch definitions.
- `V1109`: Involves blocking and reactivating a purchase order item alongside quantity changes, which fits none of the standard or churn categories directly.
- `V1117`: Long duration path with multiple master data changes (price, quantity) and approval adjustments leading to a payment block removal.
- `V1121`: Features goods receipt cancellation and replacement deep in the process flow, representing an anomaly outside normal flows.
- `V1124`: Contains goods receipt cancellations and invoice cancellations spread across a moderate duration.
- `V1311`: The narrative focuses extensively on purchase order release, approval changes, and reactivation loops, which do not cleanly fit any standard taxonomy category.
- `V1752`: Involves repeated goods receipts without a full standard invoicing loop fitting the clean flow.
- `V1759`: Involves cancellations and modifications that deviate slightly from a purely standard flow.
- `V1762`: Contains minor repetitions of goods receipts and invoices that do not cleanly fit standard flow.
- `V1763`: Unusual start with vendor invoice and late cancellation.
- `V1764`: Contains repeated goods receipts and invoice receipts creating minor churn.
- `V1765`: Multiple price and quantity changes during the execution phase.
- `V1769`: Includes blocking and reactivating purchase order items with longer duration.
- `V1770`: Contains repeated payment blocks and invoice receipts.
- `V1773`: Involves subsequent invoice cancellation and repeated clearings.
- `V1775`: Long waiting periods and payment block actions without full standard clarity.
- `V1807`: The flow is dominated by extensive approval and change churn on the purchase order without reaching the invoicing stage.
- `V1852`: Involves repeated goods receipts, invoice entries, and payment block removal which does not neatly fit standard or low touch paths.
- `V1853`: Features multiple repeated goods receipt actions leading to a clear invoice step, containing rework that falls outside standard flows.
- `V1856`: Contains quantity changes, repeated goods receipts, and payment block removals over a moderate duration.
- `V1858`: Iterative vendor invoice creation and repeated invoice receipts without standard flow predictability.
- `V1861`: Involves goods receipt cancellation and repetition anomalies.
- `V1862`: Price changes and repeated vendor invoices with moderate duration and rework.
- `V1864`: Contains duplicate vendor invoice creation and invoice receipt repetitions.
- `V1865`: Multiple iterations of vendor invoice creation and goods receipt repetitions.
- `V1868`: Repeated quantity changes and multiple modifications during the procurement path.
- `V1870`: Repeated price change events before vendor invoice and goods receipt.
- `V1871`: Extensive repetition of vendor invoices, goods receipts, and invoice receipts.
- `V1872`: Looping pattern of vendor invoices and goods receipts interspersed with invoice receipts.
- `V1873`: Contains repeated goods receipt actions within a moderate duration flow.
- `V1875`: Involves repeated goods receipts following invoice receipt steps.
- `V2029`: Does not fit standard flow or any specific anomaly category as it purely consists of repeated changes to delivery indicators without goods or invoice actions.
- `V2402`: Involves invoice receipt cancellation and a lengthy duration with rework not matching standard flow criteria.
- `V2404`: Includes service entry sheet references and cancellation anomalies not fitting simple flow categories.
- `V2410`: Short trace with cancellations and debit memos not cleanly fitting standard or low-touch flows.
- `V2412`: Extended duration and invoice cancellation pointing toward a non-standard residual flow.
- `V2413`: Involves invoice cancellations and multiple payment adjustments over an extended duration.
- `V2415`: Includes multiple invoice cancellations and debit memos outside standard flow limits.
- `V2416`: Prolonged cycle with delivery indicator changes and cancellations.
- `V2420`: Extended duration with multiple cancellations and invoice reprocessing loops.
- `V2421`: Involves repeated invoice receipts and extended duration leading to record invoice receipt outcome.
- `V2426`: This narrative involves quantity changes, multiple invoices and payments blocks with moderate duration, fitting the residual category as it does not neatly fit standard procurement, low-touch flows, service entry rework, or SRM anomalies.
- `V2427`: Complex debit memo, invoice cancellations, and repeated payment block removals form a custom rework pattern not cleanly mapped to any single specific taxonomy category.
- `V2429`: Involves multiple delivery indicator changes and standard invoice clearing, forming a minor custom variant not covered by the defined categories.
- `V2430`: Ends in a PO deletion with cancellations of both goods receipt and invoice receipt, forming part of the residual.
- `V2431`: Includes late cancellation of invoice receipts and quantity adjustments, not aligning cleanly with any main category.
- `V2432`: Features quantity changes and order confirmations leading to a standard clear invoice, but falls into the residual due to quantity rework specifics.
- `V2434`: Involves debit memos, cancellations, and payment block removals that represent a non-standard procurement exception flow.
- `V2435`: Contains subsequent invoicing, duplicate goods receipts, and multiple invoice clearings, fitting the residual category.
- `V2436`: Features repeated quantity changes and goods receipts over a moderate duration, falling outside standard clean procurement flows.
- `V2437`: Characterized by multiple quantity changes, goods receipts, and duplicate invoice receipts over a moderate timeline.
- `V2438`: Exhibits extensive repetitions of goods receipt events and subsequent invoice cancellations, placing it in the residual.
- `V2439`: Involves late repeated invoice receipts months after initial clearing, making it a unique residual case.
- `V2440`: Shows severe churn with repeated payment block removals, invoice receipts, and clearing cancellations.
- `V2441`: Exhibits multiple alternating vendor invoices, goods receipts, and repeated invoice receipts and clearings.
- `V2442`: Features price changes, debit memos, and multiple clearing loops characteristic of complex residual exception flows.
- `V2446`: Includes multiple quantity changes, delivery indicator updates, and duplicate invoices, constituting a residual exception flow.
- `V2447`: Features repeated vendor invoices and invoice receipts interspersed across different timeframes.
- `V2449`: Characterized by an extreme burst of dozens of consecutive goods receipt events, placing it in the residual.
- `V2450`: Features an extensive sequence of repeated goods receipt events by various resources, constituting a distinct anomaly outside standard definitions.
- `V2575`: Does not fit standard flow due to deletion, nor low-touch because it completes invoicing, nor extreme churn/service entries.
- `V2907`: Short sequence consisting solely of requisition, order, and repeated price changes, not fitting standard end-to-end procurement or other specific categories.
- `V2911`: Short flow ending in approval changes, not matching a full standard procurement loop.
- `V3634`: Does not fit standard flow, service entry, SRM anomalies, or extreme churn/duration patterns.
- `V3635`: Moderate duration with some invoice rework, but does not match any primary category archetype cleanly.
- `V3636`: Contains multiple price changes but lacks the typical multi-year churn or simple standard flow characteristics.
- `V3637`: Involves quantity changes and invoice rework within a moderate duration, fitting outside the defined categories.
- `V3638`: Moderate duration with quantity and delivery indicator modifications without falling into specific categories.
- `V3640`: Single long wait between invoice receipt and order confirmation, but does not fit standard categories.
- `V3641`: Multiple invoice and goods receipt iterations without extreme multi-year churn or service entry focus.
- `V3642`: Short sequence involving payment block removal and clearing, not fitting standard flow or other definitions.
- `V3645`: Involves debit memo and invoice cancellation within moderate duration.
- `V3646`: Standard sequence with a price change and payment block removal.
- `V3647`: Involves debit memo, cancel invoice receipt, and payment block handling.
- `V3648`: Features multiple cancellations of invoice receipts and debit memos.
- `V3649`: Involves goods receipt cancellation and quantity changes.
- `V4276`: This narrative shows moderate duration and some invoice/payment block clearings, but none of the specific flow patterns from the taxonomy apply cleanly.
- `V4277`: Shows repetition of goods receipts and invoices, but lacks the extreme churn or specific markers of the defined categories.
- `V4278`: Moderate duration with some quantity and invoice repetitions, not aligning tightly with any specific category definition.
- `V4279`: Contains cancellations and repetitions of goods receipts, but doesn't fit standard flows or extreme churn.
- `V4281`: Long duration and repeated invoicing/clearing steps that do not fit into the other specific categories.
- `V4282`: Extended duration with multiple goods receipts and invoice receipts, but lacks the extreme multi-year churn profile.
- `V4283`: Involves multiple vendor invoices, goods receipts, and payment blocks over a long duration, but does not fit standard or specific categories.
- `V4284`: Requisition-to-order flow with minor invoice cancellations and clearings, forming part of the residual.
- `V4285`: Short-to-moderate flow with repeated payment blocks and invoices, not fitting neatly into the main defined patterns.
- `V4286`: Contains debit memos, multiple invoice receipts, and multiple clearings over a moderate duration.
- `V4287`: Shows repeated goods and invoice receipts but otherwise follows a general procurement pattern.
- `V4288`: Involves price and quantity changes with delayed invoice receipt and clearing.
- `V4290`: Involves repeated invoicing, cancellations, and multiple clearings.
- `V4292`: Extended duration involving repeated invoices and a late invoice receipt cancellation.
- `V4366`: Does not clearly fit any standard flow due to mixed duplicate goods and invoice entries without cleanly falling into extreme duration or low-touch categories.
- `V4368`: Contains debit memos and cancellations within a moderate duration, representing a residual execution pattern.
- `V4877`: Does not fit any category cleanly due to standard sequence length but contains multiple changes and cancellations spread out.
- `V4878`: Contains multiple cancellations, debit memos, and duplicate clearing events, but is not massive enough to be extreme churn.
- `V4880`: Represents a moderate cycle with some debit memos and payment block removals, but not extensive enough for extreme churn.
- `V4883`: Contains cancellation and debit memo loops leading to order deletion, fitting none of the clean or minor flows.
- `V4884`: Involves repeated invoicing and goods receipt loops, but duration and churn are moderate.
- `V4888`: Includes repeated debit memos and cancel invoice receipts, falling outside standard or low-touch flows.
- `V4889`: Contains a delayed secondary goods receipt long after invoice clearing, fitting no primary category.
- `V4893`: Contains quantity change loops and payment blocks over a moderate timeframe.
- `V4894`: Exhibits repeated invoice receipts and goods receipts, but doesn't reach the extreme level of churn.
- `V4895`: Centered around multiple consecutive goods receipts followed by a cancellation.
- `V4896`: Involves goods receipt, cancellation, quantity change, and another receipt in a short sequence.
- `V4899`: Involves cancelled goods and invoice receipts over a long duration.
- `V4902`: Does not fit standard clean flows or extreme churn; it has moderate duration and cancellation/rework elements not neatly matching the main categories.
- `V4905`: Long duration involving a delayed duplicate invoice receipt, but not extensive enough in churn or structural anomaly to fit standard definitions.
- `V5313`: The narrative features a late delivery indicator change after significant duration and goods receipt cancellation, which falls outside the standard patterns.
- `V5315`: Features an exceptionally delayed invoice receipt resulting in an incomplete lifecycle ending on an invoice receipt without clearance.
- `V5317`: Involves out-of-order vendor invoices and multiple cancellations, ending in a canceled invoice receipt outside standard flows.
- `V5323`: Features unusual sequencing with long delays, debit memos, and a late cancellation of an invoice receipt.
- `V5324`: Involves irregular ordering of debit memos and invoices prior to the standard processing steps.
- `V5377`: This variant features a moderate-to-long duration with invoice cancellations and repetitions that do not cleanly fit the extreme multi-year churn category or standard flows.
- `V5378`: The flow contains standard invoice and goods receipt steps with minor cancellations, forming part of the residual rather than fitting a clean standard or extreme category.
- `V5379`: Involves quantity and price changes along with invoice cancellations and repeats, falling into the residual category.
- `V5380`: Contains standard purchasing steps interspersed with quantity changes and an invoice cancellation over a medium duration.
- `V5381`: Features quantity adjustments and delivery indicator changes alongside invoice processing, not matching any single strict pattern.
- `V5382`: Displays price and quantity updates followed by a delayed invoice cancellation and receipt.
- `V5383`: Involves order confirmation and payment block removal with delayed invoice clearing.
- `V5384`: Characterized by a burst of repeated goods receipt actions followed by standard invoice clearing.
- `V5385`: Features repeated goods receipts and price changes prior to payment block removal and invoice clearing.
- `V5386`: Contains multiple repetitions of goods receipts, invoice receipts, and payment block removals over a 118-day duration.
- `V5387`: Shows repeated vendor invoices, goods receipts, and multiple clearings over an extended duration.
- `V5388`: Involves quantity changes and delivery indicator modifications with duplicate vendor invoice entries.
- `V5389`: Features order item blocking and reactivation steps before goods receipt and payment clearing.
- `V5390`: Contains debit memo handling and invoice cancellations prior to final payment clearing.
- `V5391`: Dominated by an exceptionally high volume of repeated goods receipt actions before final invoicing and clearing.
- `V5534`: The trace consists mainly of repeated goods receipts and a standard completion without significant churn or extreme duration.
- `V5537`: Contains numerous repeated goods receipts but follows a relatively concise and direct purchasing path.
- `V5538`: Contains minor repeat invoicing and clearing, but does not fit cleanly into extreme churn or standard flow categories.
- `V5541`: Short process containing multiple repeat goods receipts and invoice receipts but completing relatively quickly.
- `V5544`: Involves goods receipt cancellation and quantity changes but does not display extreme overall churn.
- `V5545`: Repeated delivery indicator changes without reaching extreme duration or churn thresholds.
- `V5804`: The flow involves extended cycles, multiple repeated document changes, and non-standard loops that exceed a clean standard or simple flow.
- `V5817`: Involves extensive document cancellations, repeated changes, and multiple cycles of goods receipts and block removals exceeding a standard flow.
- `V5818`: Extensive churn with numerous repeated vendor invoices, cancellations, and multiple clearings over a long duration.
- `V5824`: High churn involving numerous repeated goods receipts, multiple vendor invoices, and several successive invoice receipt postings.
- `V5954`: Repeated loops and cancellations over 147 days fit none of the standard or simple flows cleanly.
- `V5955`: Exhibits multiple repeated invoice receipts and debit memos over a moderate duration.
- `V5956`: Involves repeated goods and invoice receipts separated by long intervals.
- `V5959`: Contains excessive repetition of goods receipts characteristic of data churn.
- `V5962`: Multiple repetitions of quantities, goods receipts, and invoices deviate from standard flows.
- `V5964`: Features repetitive cancellations and invoice clearing loops.
- `V5965`: Extensive delay and cancellations without a normal completion path.
- `V5968`: Involves multiple invoice entries and cancellations spanning several months.
- `V6977`: Does not clearly fit any standard flow, containing a mixture of quantity changes, invoice cancellations, and payment block removals.
- `V6978`: Contains repeated invoice receipts and cancellations, making it fall outside the standard procurement path.
- `V6979`: Exhibits multiple repeated goods receipts and cancellations.
- `V6980`: Anomalous sequence ending in a cancelled goods receipt with long intervals.
- `V6981`: Features repeated clearing and invoice receipt reversals.
- `V6982`: Long and complex trace with repeated invoice receipts, clearings, and goods receipt cancellations.
- `V6983`: Similar to V6982 with complex invoice reversals, multiple clearings, and modifications.
- `V6984`: Contains multiple quantity changes, repeated payment blocks, and invoice cancellations.
- `V6986`: Involves price/quantity changes and repeated invoice receipts.
- `V6987`: Contains multiple quantity changes and repeated vendor invoices.
- `V6988`: Features delayed invoice cancellations, payment block removals, and repeated invoice receipts.
- `V6989`: Unusual sequence of price and quantity changes occurring after invoice receipt.
- `V6990`: Features repeated invoice receipts, debit memos, and clearings after long delays.
- `V6991`: Involves subsequent invoice cancellation and repeated invoice clearing.
- `V6992`: Extensive repetition of invoice receipts, payment block removals, and invoice clearings.
- `V6993`: Contains multiple invoice receipts, debit memos, and cancellations.
- `V6994`: Features subsequent invoice cancellations and replacements.
- `V6995`: Involves deleting and reactivating a purchase order item along with repeated invoice processes.
- `V6996`: Contains delayed steps, quantity changes, and repeated invoice processing.
- `V6998`: Complex process involving invoice cancellations and removal of payment blocks.
- `V6999`: Features multiple quantity changes, invoice cancellations, and repeated payment block actions.
- `V7000`: Similar to V6999 with quantity changes, debit memos, cancellations, and clearings.
- `V7024`: Does not fit standard procurement, low-touch, service entry, SRM anomaly, or extreme churn; it represents a simple blocking and reactivation without invoicing.
- `V7090`: This flow includes deletion and reactivation of purchase order items mixed with delivery indicator changes, which does not fit cleanly into standard flows or extreme duration patterns.
- `V7094`: Features multiple goods receipt cancellations and debit memos without progressing to a standard invoice clearing path.
- `V7099`: Ends in a purchase order item deletion following a series of invoice cancellations and debit memos, representing an exceptional termination path.
- `V7282`: Does not fit standard flows or service entry patterns cleanly due to multiple quantity changes, payment block removals, and cancellations.
- `V7283`: Features multiple goods receipt cancellations and repeated invoice receipts without service entry dominance or standard clean flow.
- `V7286`: Involves multiple invoice cancellations, repeated payment block removals, and repeated invoice clearings outside typical category bounds.
- `V7288`: Contains multiple price changes and goods receipt cancellations not fitting standard procurement or other defined patterns.
- `V7289`: Features subsequent invoices, multiple vendor invoices, and repeated clearing actions.
- `V7290`: Involves multiple debit memos, repeated invoice clearings, and extended duration.
- `V7291`: Contains quantity changes, repeated goods receipts, and multiple invoice receipts.
- `V7292`: Exhibits complex rework including duplicate vendor invoices, repeated clearings, and delivery indicator changes.
- `V7293`: Involves order approvals, blocking, reactivating, and quantity changes.
- `V7294`: Involves order approvals, blocking, and reactivating purchase order items.
- `V7297`: Contains delayed goods receipt cancellations, quantity changes, and delivery indicator changes.
- `V7298`: Ends in a change delivery indicator with multiple quantity changes and delays.
- `V7562`: Contains multiple quantity changes, delivery indicator updates, and payment blocks with repeated invoices that fall into the residual category due to specific churn and rework elements.
- `V7564`: Contains long duration with invoice cancellations and payment blocks, which do not fit standard flows or other specific categories neatly.
- `V7566`: Involves deletion and reactivation of purchase order items combined with multiple goods receipts and price changes.
- `V7567`: Features goods receipt cancellations, invoice cancellations, and changes in delivery indicators representing non-standard rework.
- `V7569`: Contains multiple price and quantity change cycles which represent non-standard procurement modifications.
- `V7570`: Features repeated price changes and payment block removals that deviate from a standard, clean procurement flow.
- `V7571`: Includes deletion and subsequent reactivation of a purchase order item, indicating non-standard path execution.
- `V7572`: Involves multiple quantity changes, delivery indicator adjustments, and repeated goods receipts outside a standard path.
- `V7573`: Contains multiple cancellations of invoice receipts, repeated clearing steps, and debit memos.
- `V7575`: Features debit memos, invoice cancellations, and repeated changes making it a residual case.
- `V7902`: Does not fit standard clean flows or heavy churn patterns; represents a moderate duration variant with a solitary payment block release and change quantity.
- `V8650`: Does not fit standard procurement or service entry flow cleanly; ends in change quantity without full invoice clearing or low-touch completion.
- `V8735`: The flow involves extended duration, price changes, multiple invoice postings, and payment blocks which do not fit the clean or short categories.
- `V8737`: Involves multiple invoice receipts and vendor creates invoice iterations outside standard expected flows.
- `V8741`: Repeated vendor invoices and payment block removals over a moderate duration.
- `V8742`: Storage location changes and quantity modifications over a prolonged duration.
- `V8744`: Includes quantity updates, multiple invoice receipts, and payment block removals.
- `V8745`: Involves goods receipt cancellations and quantity adjustments.
- `V8747`: Includes repeated clearings and debit memos.
- `V8748`: Features out-of-order start with vendor invoice followed by purchase order creation, plus repeated clearings.
- `V8750`: Contains quantity change repetitions and duplicate invoice creation.
- `V8991`: Does not fit standard flow due to goods receipt cancellation anomaly, nor does it fit other specific categories.
- `V8999`: Involves invoice cancellations, debit memos, and item blocking which does not fit cleanly into standard flows or other categories.
- `V9053`: This variant exhibits unusual quantity adjustments and delivery indicator changes that do not cleanly match any standard or low-touch flow.
- `V9063`: Contains excessive quantity changes and mixed invoice receipts that extend beyond standard flow patterns.
- `V9064`: Characterized by recurring quantity adjustments and multiple invoice creation steps outside standard patterns.
- `V9068`: Involves multiple repeated quantity changes and multiple invoices that make it deviate from clean standard flows.
- `V9069`: Contains multiple quantity changes, repetitive invoice receipts, and removals of payment blocks indicating non-standard churn.
- `V9070`: Extended sequence with repeated quantity changes, multiple invoice receipts, and repeated clearing steps.
- `V9344`: Does not fit any category cleanly as it consists primarily of repeated delivery indicator changes with no invoice or service entry execution.
- `V9345`: Does not fit a standard flow or service entry; primarily consists of multiple goods receipts and delivery indicator changes.
- `V9356`: The process involves extended duration, invoice cancellations, and invoice removals that do not neatly fit the simpler categories.
- `V9365`: Exhibits multiple invoice cancellations, repeated receipt steps, and payment block adjustments creating a complex loop.
- `V9366`: Contains extensive cancellations, repeated invoices and debit memos, and multiple clearings that fall outside standard patterns.
- `V9370`: Contains approval changes, multiple repeated goods receipts and invoice receipts spaced far apart, rendering it non-standard.
- `V9371`: Involves multiple repeated invoices, debit memos, cancellations, and payment block toggles.
- `V9531`: The trace consists entirely of order modifications, deletion, and reactivation without completing a standard procurement or invoice cycle.
- `V10493`: Involves multiple adjustments and ends with a purchase order item deletion, not fitting cleanly into standard or short flows.
- `V10809`: This narrative involves repeated invoicing, multiple payment block removals, and duplicate invoice clearances, which do not fit cleanly into any single defined category.
- `V10821`: Involves delayed duplicate invoice receipts and clearances separated by a long duration, making it an anomaly outside standard flows.
- `V10827`: Does not fit any category clearly due to an unusual sequence ending in a storage location change without standard completion.
- `V11208`: The flow involves multiple deletions, reactivations, debit memos, and invoice clearings with cancellations, falling outside standard or simple flows.
- `V11365`: Does not fit standard procurement or rework flows as it is dominated by repetitive storage location changes culminating in deletion.
- `V11761`: This flow is strictly limited to price and quantity changes following order creation without reaching invoicing or service completions, falling outside the defined taxonomy categories.