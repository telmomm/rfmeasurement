# RF Measurement Framework --- Project Documentation

> Working project name: **rfmeasurement**\
> Working title: **An open-source framework for uncertainty-aware
> validation and reproducible analysis of RF measurements**

This directory is the living design and development specification for
the project. It is intentionally written before the implementation so
that the software architecture, scientific scope, validation strategy,
and open-source practices remain explicit as the project evolves.

## Purpose

The project aims to provide a Python framework for turning RF
measurement data into **validated, uncertainty-aware, reproducible
scientific results**.

The framework is not intended to replace
[scikit-rf](https://scikit-rf.readthedocs.io/). Instead, it should build
on established RF network-analysis functionality and add a higher-level
layer for:

-   measurement provenance;
-   measurement-quality assessment;
-   uncertainty modelling and propagation;
-   reproducible analysis;
-   machine-readable result reports;
-   validation and diagnostics;
-   research-grade experiment records.

## Design principle

> **Do not only report an RF result. Report how the result was obtained,
> how trustworthy the measurement is, and what uncertainty contributes
> to the final value.**

## Documentation map

  -------------------------------------------------------------------------------
  Document                                    Purpose
  ------------------------------------------- -----------------------------------
  [Vision and mission](vision.md)             Why the project exists

  [Scope](scope.md)                           What is and is not part of the
                                              project

  [Requirements](requirements.md)             Functional and non-functional
                                              requirements

  [Architecture](architecture.md)             Proposed software architecture

  [Domain model](domain-model.md)             Core scientific concepts and
                                              objects

  [Uncertainty](uncertainty.md)               Scientific design for uncertainty
                                              quantification

  [Measurement                                Validation and QA framework
  quality](measurement-quality.md)            

  [Reproducibility](reproducibility.md)       Provenance and experiment records

  [Roadmap](roadmap.md)                       Development phases and milestones

  [Repository                                 Proposed repository structure
  organisation](repository-organization.md)   

  [Testing and                                Verification strategy
  validation](testing-validation.md)          

  [Contributing](contributing.md)             Open-source contribution model

  [Governance](governance.md)                 Project decision-making

  [JOSS strategy](joss-strategy.md)           Design constraints for eventual
                                              JOSS submission

  [Research plan](research-plan.md)           Evidence and benchmark strategy
  -------------------------------------------------------------------------------

## Status

This is a **design-stage specification**. Decisions documented here are
provisional until implemented, tested, and reviewed through the
project's public development process.
