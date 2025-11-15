# MATLAB Compatibility Guide for qMRLab

## JavaFrame Deprecation and MATLAB 2021+ Compatibility

### Overview

As of MATLAB R2019b, the `JavaFrame` property was deprecated, and in MATLAB R2021a and newer versions, it has been progressively removed. Additionally, GUIDE (the GUI development environment) has been completely removed as of MATLAB R2025, replaced by App Designer.

This document outlines the changes made to ensure qMRLab GUI works with MATLAB 2021+ and provides a roadmap for future migration.

## Changes Implemented

### 1. Fixed JavaFrame Usage in `attachScrollPanelTo.m`

**File**: `src/Common/GUI/attachScrollPanelTo.m`

**Problem**: The function used `hPanel.JavaFrame.getGUIDEView` to create scrollable panels, which fails in MATLAB 2021+.

**Solution**:
- Wrapped JavaFrame access in try-catch blocks
- Suppressed deprecation warnings for MATLAB versions where JavaFrame still works
- Implemented graceful fallback when JavaFrame is unavailable
- The panel displays without scroll bars in MATLAB 2021+ but remains functional

**Changes**:
- Lines 94-138: Added version-safe JavaFrame access with fallback
- Lines 149-174: Conditional configuration of scroll-specific features
- Lines 199-216: Updated `repaintScrollPane()` with safety checks
- Lines 218-231: Updated `getViewOffset()` with fallback to [0,0]
- Lines 233-251: Updated `setViewOffset()` with safety checks

### 2. Added Error Handling in Main GUI

**File**: `qMRLab.m`

**Problem**: Calls to `attachScrollPanelTo()` would crash the entire GUI if JavaFrame was unavailable.

**Solution**:
- Wrapped all `attachScrollPanelTo()` calls in try-catch blocks (lines 332-350)
- Added user-friendly warnings instead of crashes
- GUI continues to function without scroll panels

## Affected Components

### GUIDE-based GUIs in qMRLab

The following GUIDE-based GUI files exist in the codebase:

1. **Main GUI**: `qMRLab.fig` / `qMRLab.m`
2. **Simulation GUIs**:
   - `Sim_MonteCarlo_Diffusion_GUI.fig`
   - `Sim_Optimize_Protocol_GUI.fig`
   - `Sim_Multi_Voxel_Distribution_GUI.fig`
   - `Sim_Sensitivity_Analysis_GUI.fig`
   - `Sim_Single_Voxel_Curve_GUI.fig`
3. **Options GUIs**:
   - `Custom_OptionsGUI.fig`
   - `MTSAT_OptionsGUI.fig`
   - `SIRFSE_OptionsGUI.fig`
   - `bSSFP_OptionsGUI.fig`

### JavaFrame Dependencies

**Core qMRLab code**:
- `src/Common/GUI/attachScrollPanelTo.m` - **FIXED**

**External dependencies** (not modified):
- `External/dicm2nii/nii_viewer.m` - Lines 610-614
- `External/imtool3D_td/imtool3D_nii.m` - Line 141
- Various Java Swing usages in External libraries

## Current Status

### ✅ Working in MATLAB 2021+

- Main qMRLab GUI launches without JavaFrame errors
- File browser panels display (without scroll bars)
- Method selection and switching works
- Options panels function correctly
- Fit data loading and viewing works

### ⚠️ Limited Functionality in MATLAB 2021+

- **Scroll bars**: Not available in file browser panels when content exceeds panel size
- **Workaround**: Resize the main window to see all content, or use newer MATLAB's built-in panel resizing

### ❌ Not Addressed (External Libraries)

- JavaFrame usage in `External/` directory files
- These are third-party libraries; users should update them independently if needed

## Migration Strategy

### Short-Term (Current Implementation) ✅

**Goal**: Make GUI functional in MATLAB 2021-2025+ without crashes

**Status**: COMPLETE

- [x] Identify all JavaFrame usage in core qMRLab code
- [x] Implement version-safe wrappers with try-catch blocks
- [x] Add graceful fallbacks for missing functionality
- [x] Test GUI launches without errors

**User Impact**: Minimal - GUI works with minor loss of scroll functionality

### Medium-Term (6-12 months)

**Goal**: Improve user experience on modern MATLAB versions

**Recommended Actions**:

1. **Alternative Scrolling Solution**
   - Investigate pure MATLAB solutions for scrollable panels
   - Consider using `uicontrol` with custom scrolling logic
   - Estimated effort: 2-3 weeks

2. **Enhanced Panel Layout**
   - Redesign panels to minimize need for scrolling
   - Use collapsible sections or tabs
   - Estimated effort: 3-4 weeks

3. **Version Detection & User Notification**
   - Add startup check for MATLAB version
   - Display one-time notice about limitations in R2021+
   - Provide link to compatibility documentation
   - Estimated effort: 1-2 days

### Long-Term (12-24 months)

**Goal**: Full migration away from GUIDE to modern MATLAB GUI framework

**Option 1: App Designer Migration** (Recommended)

**Pros**:
- Native MATLAB solution
- Modern, responsive UI components
- Better performance and compatibility
- Built-in scrolling and layout management
- Official MATLAB support

**Cons**:
- Significant development effort (estimated 3-6 months)
- All .fig files need manual conversion
- Requires learning App Designer patterns
- May break existing workflows temporarily

**Approach**:
1. Start with smaller GUIs (Options panels)
2. Create App Designer versions alongside GUIDE versions
3. Gradually migrate main GUI components
4. Provide transition period where both are available
5. Deprecate GUIDE GUIs after user testing

**Option 2: Web-Based GUI** (Alternative)

**Pros**:
- Platform independent
- Can run without MATLAB desktop
- Modern web technologies
- Better for remote/cloud usage

**Cons**:
- Even more significant effort
- Requires web development skills
- Different deployment model
- May not fit all user workflows

**Approach**:
1. Use MATLAB's `uifigure` and web components
2. Or create separate web interface using MATLAB Web App Server
3. Maintain command-line interface for all functionality

**Option 3: Hybrid Approach** (Pragmatic)

**Pros**:
- Incremental migration
- Preserves existing functionality
- Reduces risk

**Approach**:
1. Keep GUIDE GUIs for MATLAB < R2021
2. Create simplified App Designer version for R2021+
3. Focus on most-used features first
4. Maintain both versions for 2-3 years

## Transition Plan for Contributors

### For Developers Maintaining qMRLab

#### On MATLAB R2020b and Earlier

- GUIDE is still available
- Can edit .fig files directly
- JavaFrame works (with warnings)
- Full functionality available

**Workflow**:
```matlab
guide qMRLab.fig  % Opens in GUIDE editor
% Make changes and save
```

#### On MATLAB R2021a - R2024b

- GUIDE editor is deprecated but may still work
- Cannot create new GUIDE GUIs
- JavaFrame unavailable
- Use programmatic approach

**Workflow**:
```matlab
% Edit .m files directly in MATLAB Editor
% For .fig changes, use MATLAB R2020b or older on another system
% Test on R2021+ to ensure compatibility
```

#### On MATLAB R2025+

- GUIDE completely removed
- Cannot edit .fig files
- Must edit .m callback functions only
- Strong recommendation to migrate to App Designer

**Workflow**:
```matlab
% Edit .m files only
% For .fig modifications, use older MATLAB version
% Begin planning App Designer migration
```

### Extending the GUI

#### Adding New Model Parameters

**Current approach** (works on all versions):
1. Edit model class files (e.g., `src/Models/*.m`)
2. Parameters automatically appear in Options GUI
3. No .fig editing required

#### Adding New Panels or Controls

**On MATLAB ≤ R2020b**:
1. Open .fig file in GUIDE
2. Add controls visually
3. Connect callbacks in .m file
4. Test on both old and new MATLAB

**On MATLAB ≥ R2021a**:
1. Create controls programmatically in .m file
2. Use `uicontrol()` and `uipanel()` functions
3. Set positions, callbacks in code
4. Test thoroughly

**Example** (programmatic control creation):
```matlab
% In MethodMenu function or similar
hNewButton = uicontrol('Parent', handles.SomePanel, ...
                       'Style', 'pushbutton', ...
                       'String', 'New Feature', ...
                       'Units', 'normalized', ...
                       'Position', [0.1 0.1 0.3 0.05], ...
                       'Callback', @myNewCallback);
```

## Testing Checklist

### Before Committing GUI Changes

- [ ] Test on MATLAB R2019b or earlier (if available)
- [ ] Test on MATLAB R2021a or newer
- [ ] Verify no JavaFrame errors appear
- [ ] Check all panels are visible and functional
- [ ] Test model switching
- [ ] Test data loading and fitting
- [ ] Test Options GUI for multiple models
- [ ] Verify simulation GUIs work
- [ ] Check warning messages are appropriate

### Continuous Integration

Current CI should be updated to test:
- [ ] MATLAB R2020b (last version with full GUIDE)
- [ ] MATLAB R2021a (first version with JavaFrame removed)
- [ ] Latest MATLAB version (R2024b/R2025)

## Recommended Actions (Priority Order)

### Immediate (This Release)

1. ✅ Fix JavaFrame crashes
2. ✅ Add error handling
3. ✅ Create this documentation
4. ⬜ Update main README with MATLAB version compatibility info
5. ⬜ Add MATLAB version check at startup

### Next Release (3-6 months)

1. ⬜ Implement alternative scrolling solution
2. ⬜ Redesign panels to minimize scrolling needs
3. ⬜ Create App Designer prototype for one small GUI
4. ⬜ Gather user feedback on GUI priorities

### Future Releases (12+ months)

1. ⬜ Complete App Designer migration for main GUI
2. ⬜ Deprecate GUIDE GUIs with sunset date
3. ⬜ Remove GUIDE dependencies entirely

## Resources

### Documentation

- [MATLAB JavaFrame Deprecation](https://www.mathworks.com/help/matlab/creating_guis/java-ui-figures-are-deprecated.html)
- [GUIDE Migration to App Designer](https://www.mathworks.com/help/matlab/creating_guis/guide-migration-to-app-designer.html)
- [App Designer Documentation](https://www.mathworks.com/help/matlab/app-designer.html)

### Community Resources

- [Undocumented MATLAB - JavaFrame](https://undocumentedmatlab.com/articles/javaframe)
- [MATLAB Answers - GUIDE Alternatives](https://www.mathworks.com/matlabcentral/answers/)

## FAQ

### Q: Will the GUI work on MATLAB 2025?

**A**: Yes, with the fixes implemented in this release. However, scroll bars in some panels may not be available.

### Q: Can I still edit .fig files?

**A**: Only on MATLAB R2020b and earlier. For R2021+, you need access to an older MATLAB version to edit .fig files.

### Q: Should we migrate to App Designer now?

**A**: Not immediately required, but strongly recommended to plan for migration within the next 12-24 months.

### Q: What if I encounter JavaFrame errors in External/ libraries?

**A**: These are third-party libraries. You can:
1. Update to newer versions of those libraries
2. Report issues to the library authors
3. Disable/remove the affected functionality if not critical

### Q: Will command-line interface still work?

**A**: Yes! All qMRLab functionality is available via command-line interface, which is unaffected by GUIDE/JavaFrame issues.

## Contact

For questions or issues related to MATLAB compatibility:
- Open an issue on GitHub: https://github.com/qMRLab/qMRLab/issues
- Tag issues with `matlab-compatibility` label

---

**Document Version**: 1.0
**Last Updated**: 2025-11-15
**Author**: Claude (AI Assistant) via @agahkarakuzu
**Status**: Initial implementation complete
