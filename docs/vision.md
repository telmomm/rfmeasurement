# Vision and Mission

## Vision

RF measurements should be treated as scientific observations rather than
isolated files containing curves.

A researcher should be able to move from raw or imported measurement
data to a result that is:

1.  **traceable** --- its origin and processing history are known;
2.  **validated** --- known quality checks have been performed;
3.  **uncertainty-aware** --- uncertainty is attached to the measurand
    rather than added as an afterthought;
4.  **reproducible** --- another researcher can reconstruct the
    analysis;
5.  **machine-readable** --- results can be consumed by software as well
    as humans;
6.  **extensible** --- new instruments, uncertainty models and
    validation rules can be added without changing the scientific core.

## Mission

Develop a sustainable, open-source Python framework that makes rigorous
RF measurement analysis easier to perform and easier to reproduce.

The project should sit between low-level instrument interfaces and
established RF network-analysis libraries.

## Scientific premise

A measured quantity is not equivalent to a file containing an
S-parameter trace.

A defensible result should conceptually follow:

**observation → measurement context → validation → measurement model →
uncertainty propagation → derived measurand → report**

The framework therefore treats metadata, calibration state,
environmental conditions, processing steps and uncertainty models as
first-class scientific information.

## Target users

### Primary

-   RF and microwave researchers;
-   antenna and filter researchers;
-   RFIC and PCB characterization groups;
-   metrology laboratories;
-   researchers using VNAs and related instrumentation;
-   developers of experimental RF measurement pipelines.

### Secondary

-   laboratory engineers;
-   research software engineers;
-   educators teaching RF measurement;
-   users building automated measurement systems.

## Non-goals of the vision

The project does not aim to become:

-   a general-purpose circuit simulator;
-   a replacement for commercial VNA software;
-   a replacement for scikit-rf;
-   a universal instrument-control framework;
-   a machine-learning platform;
-   a database service;
-   a GUI-first application.
