# Changelog
All notable changes to this project will be documented in this file.

## [Unreleased]

### Bug Fixes 🐛
- **MATLAB R2021+ Compatibility**: Fixed JavaFrame deprecation crash
    - Updated `src/Common/GUI/attachScrollPanelTo.m` with version-safe JavaFrame access
    - Added try-catch error handling in `qMRLab.m` to prevent GUI crashes
    - Fixed JavaFrame usage in `External/dicm2nii/nii_viewer.m`
    - Fixed JavaFrame usage in `External/imtool3D_td/imtool3D_nii.m`
    - GUI now works on MATLAB R2019b through R2025+ without JavaFrame errors
    - Scroll bars and drag-and-drop unavailable in MATLAB R2021+ (graceful degradation)
    - See `MATLAB_COMPATIBILITY_GUIDE.md` for details and migration strategy

- **Mapping Toolbox Dependency**: Fixed ind2rgb8 requirement
    - Created pure MATLAB implementation in `External/imtool3D_td/src/ind2rgb8.m`
    - Eliminates dependency on Mapping Toolbox or compiled MEX files
    - Works on all platforms without compilation

- **OSF Data Download**: Fixed HTTP 308 redirect handling
    - Updated `src/Common/downloadData.m` to properly handle OSF redirects
    - Implemented waterfall download strategy: curl → wget → websave → urlwrite
    - Uses system curl/wget for most reliable redirect handling
    - Improved error messages with troubleshooting tips
    - Added retry progress indicators

### Improvements 🚀
- **Reduced Warning Spam**: Scroll panel warning now shows only once per session
    - Improved user experience by suppressing repetitive compatibility warnings
    - First-time users still get informed about MATLAB R2021+ limitations

### Documentation 📚
- Added `MATLAB_COMPATIBILITY_GUIDE.md` - comprehensive guide for MATLAB version compatibility
- Added `JAVAFRAME_FIX_SUMMARY.md` - quick reference for JavaFrame fixes
- Documented long-term migration strategy from GUIDE to App Designer

## Release [2.4.1] - 2020-09-02

## New ✨
- 🆕 model: `inversion_recovery` 
    - Add general equation fitting in addition to Barral's model.

### Improvements 🚀
- GUI (JOSS review by @mfroeling)
    - Please see changes [here](https://github.com/qMRLab/qMRLab/pull/400).
- Documentation (JOSS review by @grlee77)
    - Please see changes [here](https://github.com/qMRLab/qMRLab/pull/399)

### Bug Fixes🐛
- `FilterClas` bug [fix](https://github.com/qMRLab/qMRLab/pull/385).

### Other
- Change citation reference to JOSS paper
    - Karakuzu A., Boudreau M., Duval T.,Boshkovski T., Leppert I.R., Cabana J.F., 
    Gagnon I., Beliveau P., Pike G.B., Cohen-Adad J., Stikov N. (2020), qMRLab: 
    Quantitative MRI analysis, under one umbrella doi: 10.21105/joss.02343

## Release [2.4.0] - 2020-02-14

### New ✨
- 🆕 model: `mp2rage` 
    - Fit MP2RAGE data to create a T1map.
    - The original codebase is [here](https://github.com/JosePMarques/MP2RAGE-related-scripts).
    - Check out [qMRLab's MP2RAGE blog post](https://qmrlab.org/2019/04/08/T1-mapping-mp2rage.html) by @mathieuboudreau!
- 🆕 model: `mono_t2`
    - Fit MESE data to create a T2map.
- 🆕 simulator: `Monte-Carlo Diffusion`
    - Monte Carlo simulator for 2D diffusion is able to generate synthetic 
    diffusion signal from any 2D axon packing.
    - An MRathon project by @Yasuhik, @TomMingasson and @tanguyduval. 
- 🆕 Changelog ❤️

### Improvements 🚀
- Model: `qsm_sb` 
    - With the new echo combination implementation, `qsm_sb` can now take 
      multi-echo GRE data. 
    - An MRathon project by @jeremie-fouquet.
- Get rid of redundant buttons in GUI `Protocol` panel. 

### Bug Fixes🐛
- `qMRgenBatch` account for models w/o fixed required inputs (e.g. `mp2rage`).
- Remove old built packages from `qmrlab/mcrgui`.
- Fix `qmrlab/octjn` dependencies.

### Removed 🧹

## Release [2.3.1] - 2020-01-07

### New ✨
- 🆕 static member function: getProvenance 
    - Scrape details and add more (optional) to save sidecar `*.json` files for maps.
    - See an example use [here](https://github.com/qMRLab/qMRWrappers/blob/master/mt_sat/mt_sat_wrapper.m).
- 🆕 Docker image: `qmrlab/minimal`
    - qMRLab + Octave - Jupyter for [qMRFlow](https://github.com/qMRLab/qMRflow) pipelines.    

### Improvements 🚀
- New MATLAB/Octave env: `ISNEXTFLOW` 
    - Deals with the `load_nii` case for symlinked inputs.
    - Enforces `gzip -d --force` if `ISNEXTFLOW` 
    - Commonly used by `qMRWrappers` 

### Bug Fixes🐛
- N/A

### Removed 🧹
- N/A 

## Release [2.3.0] - 2019-05-08

### New ✨

- 🆕 model: `Processing/filtermap` 
    - Apply 2D/3D spatial filtering, primarily intended for fieldmaps. 
        - `Polynomial`
        - `Gaussian` 
        - `Median` 
        - `Spline` 
- 🆕 model: `qsm_sb` 
    - Fast quantitative susceptibility mapping:
        - `Split-Bregman` 
        - `L1 Regularization`
        - `L2 Regulatization` 
        - `No Regularization` 
        - `SHARP background filtering` 
- 🆕 model: `mt_ratio` 
    - Semi-quantitative MTR. 
- 🆕 GUI 3D toolbox:
    - An array of UI tools for the visualization and brief statistical
      inspection of the data using ROI tools. 
- 🆕 functionality `qMRgenJNB`:
    - Create a Jupyter Notebook for any model. 
    - Insert Binder Badge to the documentation. 
- 🆕 Azure release pipelines and deployment protocols:
    - Set self-hosted Azure agent to compile qMRLab and ship in a Docker image
    - `qmrlab/mcrgui`: Use qMRLab GUI in a Docker image. 
    - `qmrlab/octjn`: Use qMRLab in Octave in Jupyter Env. 
    - See `/Deploy` folder for furhter details. 
    - [qMRLab DockerHub page.](https://hub.docker.com/orgs/qmrlab)

### Improvements 🚀
- Model: `vfa_t1`:
    - Bloch simulations are added 
    - Performance improvement 
- Model: `ir_t1` 
    - Parameter descriptions are improved. 
- Model: `b1_dam`
    - Protocol descriptions has been updated. 
- `FitTempResults`:
    - Is now saved every 5 minutes instead of every 20 voxels. 
    
### Bug Fixes🐛
- GUI fixes. 

### Removed 🧹
- N/A 