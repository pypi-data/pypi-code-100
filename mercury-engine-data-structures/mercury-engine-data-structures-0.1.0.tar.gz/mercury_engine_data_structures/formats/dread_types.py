# This file was generated!
import construct

from mercury_engine_data_structures import common_types
from mercury_engine_data_structures.object import Object
from mercury_engine_data_structures.pointer_set import PointerSet

Pointer_CActor = PointerSet("CActor")
Pointer_CActorComponent = PointerSet("CActorComponent")
Pointer_CCentralUnitWeightedEdges = PointerSet("CCentralUnitWeightedEdges")
Pointer_CEmmyAutoForbiddenEdgesDef = PointerSet("CEmmyAutoForbiddenEdgesDef")
Pointer_CEmmyAutoGlobalSmartLinkDef = PointerSet("CEmmyAutoGlobalSmartLinkDef")
Pointer_CEmmyOverrideDeathPositionDef = PointerSet("CEmmyOverrideDeathPositionDef")
Pointer_CEnvironmentData_SAmbient = PointerSet("CEnvironmentData::SAmbient")
Pointer_CEnvironmentData_SBloom = PointerSet("CEnvironmentData::SBloom")
Pointer_CEnvironmentData_SCubeMap = PointerSet("CEnvironmentData::SCubeMap")
Pointer_CEnvironmentData_SDepthTint = PointerSet("CEnvironmentData::SDepthTint")
Pointer_CEnvironmentData_SFog = PointerSet("CEnvironmentData::SFog")
Pointer_CEnvironmentData_SHemisphericalLight = PointerSet("CEnvironmentData::SHemisphericalLight")
Pointer_CEnvironmentData_SIBLAttenuation = PointerSet("CEnvironmentData::SIBLAttenuation")
Pointer_CEnvironmentData_SMaterialTint = PointerSet("CEnvironmentData::SMaterialTint")
Pointer_CEnvironmentData_SPlayerLight = PointerSet("CEnvironmentData::SPlayerLight")
Pointer_CEnvironmentData_SSSAO = PointerSet("CEnvironmentData::SSSAO")
Pointer_CEnvironmentData_SToneMapping = PointerSet("CEnvironmentData::SToneMapping")
Pointer_CEnvironmentData_SVerticalFog = PointerSet("CEnvironmentData::SVerticalFog")
Pointer_CEnvironmentManager = PointerSet("CEnvironmentManager")
Pointer_CEnvironmentMusicPresets = PointerSet("CEnvironmentMusicPresets")
Pointer_CEnvironmentSoundPresets = PointerSet("CEnvironmentSoundPresets")
Pointer_CEnvironmentVisualPresets = PointerSet("CEnvironmentVisualPresets")
Pointer_CLogicCamera = PointerSet("CLogicCamera")
Pointer_CScenario = PointerSet("CScenario")
Pointer_CSubAreaManager = PointerSet("CSubAreaManager")
Pointer_CSubareaCharclassGroup = PointerSet("CSubareaCharclassGroup")
Pointer_CSubareaInfo = PointerSet("CSubareaInfo")
Pointer_CSubareaSetup = PointerSet("CSubareaSetup")
Pointer_CTriggerComponent_SActivationCondition = PointerSet("CTriggerComponent::SActivationCondition")
Pointer_CTriggerLogicAction = PointerSet("CTriggerLogicAction")
Pointer_CXParasiteBehavior = PointerSet("CXParasiteBehavior")
Pointer_base_global_CFilePathStrId = PointerSet("base::global::CFilePathStrId")
Pointer_base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_ = PointerSet("base::global::CRntSmallDictionary<base::global::CStrId, CActorComponent*>")
Pointer_base_global_CRntVector_CEnvironmentData_SAmbientTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SAmbientTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SBloomTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SBloomTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SCubeMapTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SCubeMapTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SDepthTintTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SDepthTintTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SFogTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SFogTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SHemisphericalLightTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SIBLAttenuationTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SMaterialTintTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SPlayerLightTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SSSAOTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SSSAOTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SToneMappingTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SToneMappingTransition>")
Pointer_base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_ = PointerSet("base::global::CRntVector<CEnvironmentData::SVerticalFogTransition>")
Pointer_base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__ = PointerSet("base::global::CRntVector<std::unique_ptr<CSubareaCharclassGroup>>")
Pointer_base_global_CRntVector_std_unique_ptr_CSubareaSetup__ = PointerSet("base::global::CRntVector<std::unique_ptr<CSubareaSetup>>")
Pointer_base_reflection_CTypedValue = PointerSet("base::reflection::CTypedValue")
Pointer_game_logic_collision_CCollider = PointerSet("game::logic::collision::CCollider")
Pointer_game_logic_collision_CShape = PointerSet("game::logic::collision::CShape")


base_core_CBaseObject = Object(base_core_CBaseObjectFields := {})

CGameObject = Object(CGameObjectFields := base_core_CBaseObjectFields)

game_logic_collision_CBroadphaseObject = Object(game_logic_collision_CBroadphaseObjectFields := {
    **CGameObjectFields,
    "sId": common_types.UInt,
    "sStrId": common_types.StrId,
})

game_logic_collision_CShape = Object(game_logic_collision_CShapeFields := {
    "vPos": common_types.CVector3D,
    "bIsSolid": construct.Flag,
})

game_logic_collision_CCollider = Object({
    **game_logic_collision_CBroadphaseObjectFields,
    "pShape": Pointer_game_logic_collision_CShape.create_construct(),
})

CActorComponent = Object(CActorComponentFields := CGameObjectFields)

base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_ = common_types.make_dict(Pointer_CActorComponent.create_construct())

CActor = Object(CActorFields := {
    **CGameObjectFields,
    "sName": common_types.StrId,
    "oActorDefLink": common_types.StrId,
    "sActorDefName": common_types.StrId,
    "vPos": common_types.CVector3D,
    "vAng": common_types.CVector3D,
    "pComponents": Pointer_base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_.create_construct(),
    "bEnabled": construct.Flag,
})

CActorSublayer = Object({
    "sName": common_types.StrId,
    "dctActors": common_types.make_dict(Pointer_CActor.create_construct()),
})

CActorLayer = Object({
    "dctSublayers": common_types.make_dict(CActorSublayer),
    "dctActorGroups": common_types.make_dict(common_types.make_vector(common_types.StrId)),
})

CScenario = Object({
    **CGameObjectFields,
    "awpScenarioColliders": common_types.make_vector(Pointer_game_logic_collision_CCollider.create_construct()),
    "sLevelID": common_types.StrId,
    "sScenarioID": common_types.StrId,
    "rEntitiesLayer": CActorLayer,
    "rSoundsLayer": CActorLayer,
    "rLightsLayer": CActorLayer,
    "vLayerFiles": common_types.make_vector(common_types.StrId),
})

CSubareaInfo = Object({
    "sId": common_types.StrId,
    "sSetupId": common_types.StrId,
    "sPackSetId": common_types.StrId,
    "bDisableSubArea": construct.Flag,
    "fCameraZDistance": common_types.Float,
    "bIgnoreMetroidCameraOffsets": construct.Flag,
    "sCharclassGroupId": common_types.StrId,
    "asItemsIds": common_types.make_vector(common_types.StrId),
    "vsCameraCollisionsIds": common_types.make_vector(common_types.StrId),
    "vsCutscenesIds": common_types.make_vector(common_types.StrId),
})

CSubareaSetup = Object({
    "sId": common_types.StrId,
    "vSubareaConfigs": common_types.make_vector(Pointer_CSubareaInfo.create_construct()),
})

base_global_CRntVector_std_unique_ptr_CSubareaSetup__ = common_types.make_vector(Pointer_CSubareaSetup.create_construct())

CSubareaCharclassGroup = Object({
    "sId": common_types.StrId,
    "vsCharClassesIds": common_types.make_vector(common_types.StrId),
})

base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__ = common_types.make_vector(Pointer_CSubareaCharclassGroup.create_construct())

CSubAreaManager = Object({
    "vSubareaSetups": Pointer_base_global_CRntVector_std_unique_ptr_CSubareaSetup__.create_construct(),
    "vCharclassGroups": Pointer_base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__.create_construct(),
})

CEnvironmentData_SFog = Object({
    "tColor": common_types.CVector4D,
    "fColorInterp": common_types.Float,
    "fScale": common_types.Float,
    "fScaleInterp": common_types.Float,
    "tRange": common_types.CVector2D,
    "fRangeInterp": common_types.Float,
    "fWaveFreq": common_types.Float,
    "fWaveAmp": common_types.Float,
    "fWaveVelocity": common_types.Float,
    "fWaveInterp": common_types.Float,
})

CEnvironmentData_SVerticalFog = Object({
    "bEnabled": construct.Flag,
    "tColor": common_types.CVector4D,
    "fColorInterp": common_types.Float,
    "fBase": common_types.Float,
    "fBaseInterp": common_types.Float,
    "tAttenuation": common_types.CVector2D,
    "fAttInterp": common_types.Float,
    "fNear": common_types.Float,
    "fNearInterp": common_types.Float,
    "fFar": common_types.Float,
    "fFarInterp": common_types.Float,
    "fWaveFreq": common_types.Float,
    "fWaveAmp": common_types.Float,
    "fWaveVelocity": common_types.Float,
    "fWaveInterp": common_types.Float,
})

STransition = Object(STransitionFields := {})

CEnvironmentData_SFogTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorInterp": common_types.Float,
    "fScaleInterp": common_types.Float,
    "fRangeInterp": common_types.Float,
    "fWaveInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SFogTransition_ = common_types.make_vector(CEnvironmentData_SFogTransition)

CEnvironmentData_SAmbient = Object({
    "tColor": common_types.CVector4D,
    "fColorInterp": common_types.Float,
})

CEnvironmentData_SAmbientTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SAmbientTransition_ = common_types.make_vector(CEnvironmentData_SAmbientTransition)

CEnvironmentData_SDepthTint = Object({
    "fTintInterp": common_types.Float,
    "fLight": common_types.Float,
    "fCube": common_types.Float,
    "fDepth": common_types.Float,
    "fSaturation": common_types.Float,
    "fLightNear": common_types.Float,
    "fCubeNear": common_types.Float,
    "fDepthNear": common_types.Float,
    "fSaturationNear": common_types.Float,
})

CEnvironmentData_SDepthTintTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fTintInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SDepthTintTransition_ = common_types.make_vector(CEnvironmentData_SDepthTintTransition)

CEnvironmentData_SMaterialTint = Object({
    "tColor": common_types.CVector4D,
    "fColorInterp": common_types.Float,
    "fBlend": common_types.Float,
    "fBlendInterp": common_types.Float,
})

CEnvironmentData_SMaterialTintTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorInterp": common_types.Float,
    "fBlendInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_ = common_types.make_vector(CEnvironmentData_SMaterialTintTransition)

CEnvironmentData_SPlayerLight = Object({
    "tDiffuse": common_types.CVector4D,
    "tSpecular0": common_types.CVector4D,
    "tSpecular1": common_types.CVector4D,
    "fColorInterp": common_types.Float,
    "tAttenuation": common_types.CVector2D,
    "fAttenuationInterp": common_types.Float,
})

CEnvironmentData_SPlayerLightTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorInterp": common_types.Float,
    "fAttenuationInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_ = common_types.make_vector(CEnvironmentData_SPlayerLightTransition)

CEnvironmentData_SHemisphericalLight = Object({
    "tColorUp": common_types.CVector3D,
    "fColorUpInterp": common_types.Float,
    "tColorDown": common_types.CVector3D,
    "fColorDownInterp": common_types.Float,
})

CEnvironmentData_SHemisphericalLightTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorUpInterp": common_types.Float,
    "fColorDownInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_ = common_types.make_vector(CEnvironmentData_SHemisphericalLightTransition)

CEnvironmentData_SBloom = Object({
    "tBloom": common_types.CVector3D,
    "fBloomInterp": common_types.Float,
})

CEnvironmentData_SBloomTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fBloomInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SBloomTransition_ = common_types.make_vector(CEnvironmentData_SBloomTransition)

CEnvironmentData_SVerticalFogTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fColorInterp": common_types.Float,
    "fBaseInterp": common_types.Float,
    "fNearInterp": common_types.Float,
    "fFarInterp": common_types.Float,
    "fAttInterp": common_types.Float,
    "fWaveInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_ = common_types.make_vector(CEnvironmentData_SVerticalFogTransition)

CEnvironmentData_SCubeMap = Object({
    "fInterp": common_types.Float,
    "bEnabled": construct.Flag,
    "sTexturePath": common_types.StrId,
})

CEnvironmentData_SCubeMapTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fCubeMapInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SCubeMapTransition_ = common_types.make_vector(CEnvironmentData_SCubeMapTransition)

CEnvironmentData_SSSAO = Object({
    "fFallOff": common_types.Float,
    "fIntensity": common_types.Float,
    "fBias": common_types.Float,
    "fRadius": common_types.Float,
    "fDepthFct": common_types.Float,
    "bEnabled": construct.Flag,
    "fInterp": common_types.Float,
    "fIntensityFactor": common_types.Float,
    "fFogFactor": common_types.Float,
})

CEnvironmentData_SSSAOTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SSSAOTransition_ = common_types.make_vector(CEnvironmentData_SSSAOTransition)

CEnvironmentData_SToneMapping = Object({
    "fInterp": common_types.Float,
    "fExposure": common_types.Float,
    "fGamma": common_types.Float,
    "fSaturationColor": common_types.Float,
    "fContrast": common_types.Float,
    "fBrightness": common_types.Float,
    "vColorTint": common_types.CVector4D,
    "fColorVibrance": common_types.Float,
    "bEnabled": construct.Flag,
})

CEnvironmentData_SToneMappingTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SToneMappingTransition_ = common_types.make_vector(CEnvironmentData_SToneMappingTransition)

CEnvironmentData_SIBLAttenuation = Object({
    "fInterp": common_types.Float,
    "fCubeAttFactor": common_types.Float,
    "fZDistance": common_types.Float,
    "fGradientSize": common_types.Float,
})

CEnvironmentData_SIBLAttenuationTransition = Object({
    **STransitionFields,
    "sPreset": common_types.StrId,
    "fInterp": common_types.Float,
})

base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_ = common_types.make_vector(CEnvironmentData_SIBLAttenuationTransition)

CEnvironmentData = Object({
    "sID": common_types.StrId,
    "tFog": Pointer_CEnvironmentData_SFog.create_construct(),
    "tVerticalFog": Pointer_CEnvironmentData_SVerticalFog.create_construct(),
    "tFogTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SFogTransition_.create_construct(),
    "tAmbient": Pointer_CEnvironmentData_SAmbient.create_construct(),
    "tAmbientTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SAmbientTransition_.create_construct(),
    "tDepthTint": Pointer_CEnvironmentData_SDepthTint.create_construct(),
    "tDepthTintTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SDepthTintTransition_.create_construct(),
    "tMaterialTint": Pointer_CEnvironmentData_SMaterialTint.create_construct(),
    "tMaterialTintTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_.create_construct(),
    "tPlayerLight": Pointer_CEnvironmentData_SPlayerLight.create_construct(),
    "tPlayerLightTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_.create_construct(),
    "tHemisphericalLight": Pointer_CEnvironmentData_SHemisphericalLight.create_construct(),
    "tHemisphericalLightTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_.create_construct(),
    "tBloom": Pointer_CEnvironmentData_SBloom.create_construct(),
    "tBloomTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SBloomTransition_.create_construct(),
    "tVerticalFogTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_.create_construct(),
    "tCubeMap": Pointer_CEnvironmentData_SCubeMap.create_construct(),
    "tCubeMapTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SCubeMapTransition_.create_construct(),
    "tSSAO": Pointer_CEnvironmentData_SSSAO.create_construct(),
    "tSSAOTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SSSAOTransition_.create_construct(),
    "tToneMapping": Pointer_CEnvironmentData_SToneMapping.create_construct(),
    "tToneMappingTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SToneMappingTransition_.create_construct(),
    "tIBLAttenuation": Pointer_CEnvironmentData_SIBLAttenuation.create_construct(),
    "tIBLAttenuationTransitions": Pointer_base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_.create_construct(),
})

CEnvironmentVisualPresets = Object({
    "dicPresets": common_types.make_dict(CEnvironmentData),
})

CEnvironmentSoundData_SSound = Object({
    "sToPreset": common_types.StrId,
    "fVolume": common_types.Float,
    "fFadeIn": common_types.Float,
    "fFadeOut": common_types.Float,
    "fFadeInDelay": common_types.Float,
    "eReverb": common_types.UInt,
})

CEnvironmentSoundData = Object({
    "sID": common_types.StrId,
    "sSoundID": common_types.StrId,
    "tSound": CEnvironmentSoundData_SSound,
    "dctTransitions": common_types.make_dict(CEnvironmentSoundData_SSound),
})

CEnvironmentSoundPresets = Object({
    "dicPresets": common_types.make_dict(CEnvironmentSoundData),
})

sound_TMusicFile = Object({
    "sWav": common_types.StrId,
    "iLoops": common_types.Int,
    "iLoopStart": common_types.Int,
    "iLoopEnd": common_types.Int,
})

sound_TMusicTrack = Object({
    "iTrack": common_types.Int,
    "vFiles": common_types.make_vector(sound_TMusicFile),
    "fFadeIn": common_types.Float,
    "fFadeOut": common_types.Float,
    "fDelay": common_types.Float,
    "fVol": common_types.Float,
    "iStartPos": common_types.Int,
    "eCrossFade": common_types.UInt,
    "bPauseOnPop": construct.Flag,
    "fEnvFactor": common_types.Float,
})

sound_TScenarioMusicPreset = Object({
    "sAlias": common_types.StrId,
    "vTracks": common_types.make_vector(sound_TMusicTrack),
})

CEnvironmentMusicData_SMusicTransition = Object({
    "sPreset": common_types.StrId,
    "fFadeIn": common_types.Float,
    "fFadeOut": common_types.Float,
    "eFadeType": common_types.UInt,
    "ePlayFlag": common_types.UInt,
})

CEnvironmentMusicData = Object({
    "sID": common_types.StrId,
    "tPreset": sound_TScenarioMusicPreset,
    "ePlayFlag": common_types.UInt,
    "tMusicTransitions": common_types.make_vector(CEnvironmentMusicData_SMusicTransition),
})

sound_SStateFadeOut = Object({
    "eState": common_types.UInt,
    "fFadeOut": common_types.Float,
})

sound_TBossMusicTrack = Object({
    "oTrack": sound_TMusicTrack,
    "vFadeOuts": common_types.make_vector(sound_SStateFadeOut),
})

sound_TBossMusicSubStateConfig = Object({
    "eState": common_types.StrId,
    "vTracks": common_types.make_vector(sound_TBossMusicTrack),
})

sound_TBossMusicSpawnGroupConfig = Object({
    "sSpawnGroup": common_types.StrId,
    "dicSubStatePresets": common_types.make_dict(sound_TBossMusicSubStateConfig),
})

sound_TBossMusicPreset = Object({
    "sBoss": common_types.StrId,
    "dicSpawnGroupConfigs": common_types.make_dict(sound_TBossMusicSpawnGroupConfig),
})

CEnvironmentMusicPresets = Object({
    "dicPresets": common_types.make_dict(CEnvironmentMusicData),
    "dicBossPresets": common_types.make_dict(sound_TBossMusicPreset),
})

CEnvironmentManager = Object({
    "pVisualPresets": Pointer_CEnvironmentVisualPresets.create_construct(),
    "pSoundPresets": Pointer_CEnvironmentSoundPresets.create_construct(),
    "pMusicPresets": Pointer_CEnvironmentMusicPresets.create_construct(),
})

gameeditor_CGameModelRoot = Object({
    "pScenario": Pointer_CScenario.create_construct(),
    "pSubareaManager": Pointer_CSubAreaManager.create_construct(),
    "pEnvironmentManager": Pointer_CEnvironmentManager.create_construct(),
})

base_spatial_CAABox = Object({
    "Min": common_types.CVector3D,
    "Max": common_types.CVector3D,
})

CEntity = Object({
    **CActorFields,
    "oBBox": base_spatial_CAABox,
    "bIsInFrustum": construct.Flag,
})

CComponent = Object(CComponentFields := {
    **CActorComponentFields,
    "bEnabled": construct.Flag,
    "bWantsEnabled": construct.Flag,
    "bUseDefaultValues": construct.Flag,
})

CAttackComponent = Object(CAttackComponentFields := {
    **CComponentFields,
    "bRotateToDamagedEntity": construct.Flag,
    "fRotateToDamagedEntityMaxAngle": common_types.Float,
    "fRotateToDamagedEntityMinAngle": common_types.Float,
})

CAIAttackComponent = Object(CAIAttackComponentFields := CAttackComponentFields)

SFallBackPath = Object({
    "wpPath": common_types.StrId,
    "ePathType": common_types.UInt,
})

CAIComponent = Object(CAIComponentFields := {
    **CComponentFields,
    "sForcedAttack": common_types.StrId,
    "iForcedAttackPreset": common_types.Int,
    "fTimeSinceTargetLastSeen": common_types.Float,
    "fTimeSinceLastDamage": common_types.Float,
    "fTimeSinceLastFrozen": common_types.Float,
    "fPathLeftCut": common_types.Float,
    "fPathRightCut": common_types.Float,
    "fCutDistanceClockwise": common_types.Float,
    "fCutDistanceCounterClockwise": common_types.Float,
    "wpPathToFollow": common_types.StrId,
    "tFallbackPaths": common_types.make_vector(SFallBackPath),
    "ePathType": common_types.UInt,
    "bIndividualRequiresActivationPerception": construct.Flag,
    "bIgnoreAttack": construct.Flag,
    "bInBlindAttack": construct.Flag,
})

CGrapplePointComponent = Object(CGrapplePointComponentFields := CComponentFields)

CPullableGrapplePointComponent = Object(CPullableGrapplePointComponentFields := CGrapplePointComponentFields)

CAIGrapplePointComponent = Object(CPullableGrapplePointComponentFields)

CAINavigationComponent = Object(CComponentFields)

CAISmartObjectComponent = Object({
    **CComponentFields,
    "fResetTime": common_types.Float,
    "fUseTime": common_types.Float,
    "iSpawnDirection": common_types.Int,
})

CAbilityComponent = Object({
    **CComponentFields,
    "bAccurateAiming": construct.Flag,
    "sBlockSyncFX": common_types.StrId,
})

CUsableComponent = Object(CUsableComponentFields := {
    **CComponentFields,
    "bFadeInActived": construct.Flag,
})

CAccessPointComponent = Object(CAccessPointComponentFields := {
    **CUsableComponentFields,
    "vDoorsToChange": common_types.make_vector(common_types.StrId),
    "sInteractionLiteralID": common_types.StrId,
    "tCaptionList": common_types.make_dict(common_types.make_vector(common_types.StrId)),
    "wpThermalDevice": common_types.StrId,
})

CAccessPointCommanderComponent = Object({
    **CAccessPointComponentFields,
    "wpAfterFirstDialogueScenePlayer": common_types.StrId,
})

CActivatableComponent = Object(CActivatableComponentFields := CComponentFields)

CActionSwitcherComponent = Object(CActivatableComponentFields)

CActionSwitcherOnPullGrapplePointComponent = Object({
    **CPullableGrapplePointComponentFields,
    "sActionOnPull": common_types.StrId,
})

CActivatableByProjectileComponent = Object(CActivatableByProjectileComponentFields := CComponentFields)

CAimCameraEnabledVisibleOnlyComponent = Object(CComponentFields)

CAimComponent = Object({
    **CComponentFields,
    "sLaserFX": common_types.StrId,
    "sAutoAimLaserFX": common_types.StrId,
    "bAutoAimActive": construct.Flag,
    "bLockOnSoundAllowed": construct.Flag,
    "fCurrentAutoAimWidth": common_types.Float,
    "fCurrentAutoAimConeLength": common_types.Float,
})

CAlternativeActionPlayerComponent = Object(CAlternativeActionPlayerComponentFields := CComponentFields)

CAmmoRechargeComponent = Object({
    **CUsableComponentFields,
    "sRechargeFX": common_types.StrId,
    "sEyeRFX": common_types.StrId,
    "sEyeLFX": common_types.StrId,
})

CAnimationComponent = Object(CAnimationComponentFields := CComponentFields)

CNavMeshItemComponent = Object(CNavMeshItemComponentFields := {
    **CComponentFields,
    "tForbiddenEdgesSpawnPoints": common_types.make_vector(common_types.StrId),
})

CAnimationNavMeshItemComponent = Object(CNavMeshItemComponentFields)

CBehaviorTreeAIComponent = Object(CBehaviorTreeAIComponentFields := CAIComponentFields)

CArachnusAIComponent = Object(CBehaviorTreeAIComponentFields)

CSceneComponent = Object(CSceneComponentFields := CComponentFields)

CAreaFXComponent = Object({
    **CSceneComponentFields,
    "sModelResPath": common_types.StrId,
})

CBaseTriggerComponent = Object(CBaseTriggerComponentFields := {
    **CActivatableComponentFields,
    "bCheckAllEntities": construct.Flag,
})

CSoundTrigger = Object(CSoundTriggerFields := {
    **CBaseTriggerComponentFields,
    "eReverb": common_types.UInt,
    "iLowPassFilter": common_types.UInt,
})

CAreaMusicComponent = Object({
    **CSoundTriggerFields,
    "fEnterFadeIn": common_types.Float,
    "fEnterFadeOut": common_types.Float,
    "fExitFadeIn": common_types.Float,
    "fExitFadeOut": common_types.Float,
    "sPreset": common_types.StrId,
    "eEnterFadeType": common_types.UInt,
    "eExitFadeType": common_types.UInt,
})

CAreaSoundComponent = Object({
    **CSoundTriggerFields,
    "sOnEnterSound": common_types.StrId,
    "eOnEnterSoundType": common_types.UInt,
    "fEnterVol": common_types.Float,
    "fEnterPitch": common_types.Float,
    "fEnterFadeInTime": common_types.Float,
    "fEnterFadeOutTime": common_types.Float,
    "eOnEnterPositional": common_types.UInt,
    "sLoopSound": common_types.StrId,
    "eLoopSoundType": common_types.UInt,
    "fLoopVol": common_types.Float,
    "fLoopPitch": common_types.Float,
    "fLoopPan": common_types.Float,
    "fLoopFadeInTime": common_types.Float,
    "fLoopFadeOutTime": common_types.Float,
    "sOnExitSound": common_types.StrId,
    "eOnExitSoundType": common_types.UInt,
    "fExitVol": common_types.Float,
    "fExitPitch": common_types.Float,
    "fExitFadeInTime": common_types.Float,
    "fExitFadeOutTime": common_types.Float,
    "eOnExitPositional": common_types.UInt,
})

CAudioComponent = Object(CComponentFields)

CRobotAIComponent = Object(CRobotAIComponentFields := CBehaviorTreeAIComponentFields)

CAutclastAIComponent = Object(CRobotAIComponentFields)

CAutectorAIComponent = Object({
    **CRobotAIComponentFields,
    "eJumpType": common_types.UInt,
})

CLifeComponent = Object(CLifeComponentFields := {
    **CComponentFields,
    "bWantsCameraFXPreset": construct.Flag,
    "fMaxLife": common_types.Float,
    "fCurrentLife": common_types.Float,
    "bCurrentLifeLocked": construct.Flag,
})

CCharacterLifeComponent = Object(CCharacterLifeComponentFields := {
    **CLifeComponentFields,
    "sImpactAnim": common_types.StrId,
    "sDeadAnim": common_types.StrId,
})

CEnemyLifeComponent = Object(CEnemyLifeComponentFields := {
    **CCharacterLifeComponentFields,
    "sImpactBackAnim": common_types.StrId,
    "sDeadBackAnim": common_types.StrId,
    "sDeadAirAnim": common_types.StrId,
    "sDeadAirBackAnim": common_types.StrId,
})

CAutectorLifeComponent = Object(CEnemyLifeComponentFields)

CAutomperAIComponent = Object(CRobotAIComponentFields)

CAutoolAIComponent = Object({
    **CRobotAIComponentFields,
    "vAISmartObjects": common_types.make_vector(common_types.StrId),
})

CAutsharpAIComponent = Object(CRobotAIComponentFields)

CAutsharpLifeComponent = Object(CEnemyLifeComponentFields)

CSpawnerActorBlueprint = Object({
    "InnerValue": Pointer_base_reflection_CTypedValue.create_construct(),
})

CSpawnPointComponent = Object(CSpawnPointComponentFields := {
    **CComponentFields,
    "sOnBeforeGenerate": common_types.StrId,
    "sOnEntityGenerated": common_types.StrId,
    "sStartAnimation": common_types.StrId,
    "bSpawnOnFloor": construct.Flag,
    "bEntityCheckFloor": construct.Flag,
    "bCheckCollisions": construct.Flag,
    "fTimeToActivate": common_types.Float,
    "iMaxNumToGenerate": common_types.Int,
    "bAllowSpawnInFrustum": construct.Flag,
    "bStartEnabled": construct.Flag,
    "bAutomanaged": construct.Flag,
    "wpSceneShapeId": common_types.StrId,
    "wpCollisionSceneShapeId": common_types.StrId,
    "wpNavigableShape": common_types.StrId,
    "wpAreaOfInterest": common_types.StrId,
    "wpAreaOfInterestEnd": common_types.StrId,
    "fTimeOnAOIEndToUseAsMainAOI": common_types.Float,
    "fSpawnFromXCellProbability": common_types.Float,
    "fSpawnFromXCellProbabilityAfterFirst": common_types.Float,
    "eXCellSpawnPositionMode": common_types.UInt,
    "bUseDynamicSpawnPosition": construct.Flag,
    "eDynamicSpawnPositionMode": common_types.UInt,
    "tDynamicSpawnPositions": common_types.make_vector(common_types.StrId),
    "tXCellTransformTargets": common_types.make_vector(common_types.StrId),
    "wpXCellActivationAreaShape": common_types.StrId,
    "sCharClass": common_types.StrId,
    "voActorBlueprint": common_types.make_vector(CSpawnerActorBlueprint),
})

CAutsharpSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "eSpawnDir": common_types.UInt,
    "wpSpawnShape": common_types.StrId,
})

CAutsniperAIComponent = Object(CRobotAIComponentFields)

CAutsniperSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "eSpawnDir": common_types.UInt,
})

CBTObserverComponent = Object(CActorComponentFields)

CBossAIComponent = Object(CBossAIComponentFields := {
    **CBehaviorTreeAIComponentFields,
    "sArenaLeftLandmark": common_types.StrId,
    "sArenaRightLandmark": common_types.StrId,
    "fArenaLimitDist": common_types.Float,
    "tDoors": common_types.make_vector(common_types.StrId),
    "wpBossCamera": common_types.StrId,
    "wpBossCameraFloorLandmark": common_types.StrId,
    "wpBossCameraCeilingLandmark": common_types.StrId,
    "wpStartCombatCheckpointStartPoint": common_types.StrId,
    "sStartCombatCheckpointSnapshotId": common_types.StrId,
    "wpDeadCheckpointStartPoint": common_types.StrId,
    "bSaveGameOnAfterDead": construct.Flag,
})

CBaseBigFistAIComponent = Object(CBaseBigFistAIComponentFields := {
    **CBossAIComponentFields,
    "fMinTimeBetweenDigs": common_types.Float,
    "fMaxTimeBetweenDigs": common_types.Float,
    "fMinTimeDigging": common_types.Float,
    "fMaxTimeDigging": common_types.Float,
})

CBaseDamageTriggerComponent = Object(CBaseDamageTriggerComponentFields := {
    **CBaseTriggerComponentFields,
    "sContinuousDamageSound": common_types.StrId,
})

CBaseGroundShockerAIComponent = Object(CBaseGroundShockerAIComponentFields := CBehaviorTreeAIComponentFields)

CBaseLightComponent = Object(CBaseLightComponentFields := {
    **CComponentFields,
    "vLightPos": common_types.CVector3D,
    "fIntensity": common_types.Float,
    "fVIntensity": common_types.Float,
    "fFIntensity": common_types.Float,
    "vAmbient": common_types.CVector4D,
    "vDiffuse": common_types.CVector4D,
    "vSpecular0": common_types.CVector4D,
    "vSpecular1": common_types.CVector4D,
    "bVertexLight": construct.Flag,
    "eLightPreset": common_types.UInt,
    "vLightPresetParams": common_types.CVector4D,
    "bSubstractive": construct.Flag,
    "bUseFaceCull": construct.Flag,
    "bUseSpecular": construct.Flag,
})

CBasicLifeComponent = Object(CBasicLifeComponentFields := CLifeComponentFields)

CBatalloonAIComponent = Object({
    **CBaseGroundShockerAIComponentFields,
    "bReceivingCall": construct.Flag,
})

CItemLifeComponent = Object(CItemLifeComponentFields := CLifeComponentFields)

SBeamBoxActivatable = Object({
    "oActivatableObj": common_types.StrId,
    "sState": common_types.StrId,
})

CBeamBoxComponent = Object({
    **CItemLifeComponentFields,
    "fDisplaceDist": common_types.Float,
    "vActivatables": common_types.make_vector(SBeamBoxActivatable),
    "sAnimationId": common_types.StrId,
})

CDoorShieldLifeComponent = Object(CDoorShieldLifeComponentFields := {
    **CItemLifeComponentFields,
    "fDamageFXTime": common_types.Float,
    "sDamageSound": common_types.StrId,
    "sKillSound": common_types.StrId,
    "eColor": common_types.UInt,
})

CBeamDoorLifeComponent = Object(CDoorShieldLifeComponentFields)

CBigFistAIComponent = Object({
    **CBaseBigFistAIComponentFields,
    "timeForNextDig": common_types.Float,
})

CBigkranXAIComponent = Object(CBaseBigFistAIComponentFields)

CCollisionComponent = Object(CCollisionComponentFields := CComponentFields)

CBillboardCollisionComponent = Object(CCollisionComponentFields)

CBillboardComponent = Object({
    **CComponentFields,
    "iNumGroups": common_types.Int,
    "iMaxInhabitantsPerGroup": common_types.Int,
    "iMinInhabitantsPerGroup": common_types.Int,
})

CBillboardLifeComponent = Object(CLifeComponentFields)

CMovementComponent = Object(CMovementComponentFields := {
    **CComponentFields,
    "bIsFlying": construct.Flag,
})

CWeaponMovement = Object(CWeaponMovementFields := CMovementComponentFields)

CBombMovement = Object(CBombMovementFields := {
    **CWeaponMovementFields,
    "sCollisionFX": common_types.StrId,
})

CBoneToConstantComponent = Object(CSceneComponentFields)

CBossLifeComponent = Object(CEnemyLifeComponentFields)

CSpawnGroupComponent = Object(CSpawnGroupComponentFields := {
    **CComponentFields,
    "bIsGenerator": construct.Flag,
    "bIsInfinite": construct.Flag,
    "iMaxToGenerate": common_types.Int,
    "iMaxSimultaneous": common_types.Int,
    "fGenerateEvery": common_types.Float,
    "sOnBeforeGenerateEntity": common_types.StrId,
    "sOnEntityGenerated": common_types.StrId,
    "sOnEnable": common_types.StrId,
    "sOnDisable": common_types.StrId,
    "sOnMaxSimultaneous": common_types.StrId,
    "sOnMaxGenerated": common_types.StrId,
    "sOnEntityDead": common_types.StrId,
    "sOnEntityDamaged": common_types.StrId,
    "sOnAllEntitiesDead": common_types.StrId,
    "bAutomanaged": construct.Flag,
    "bDisableOnAllDead": construct.Flag,
    "bAutoenabled": construct.Flag,
    "bSpawnPointsNotInFrustrum": construct.Flag,
    "bGenerateEntitiesByOrder": construct.Flag,
    "sLogicCollisionShapeID": common_types.StrId,
    "wpAreaOfInterest": common_types.StrId,
    "wpAreaOfInterestEnd": common_types.StrId,
    "fDropAmmoProb": common_types.Float,
    "iInitToGenerate": common_types.Int,
    "sArenaId": common_types.StrId,
    "bCheckActiveDrops": construct.Flag,
    "iNumDeaths": common_types.Int,
    "vectSpawnPoints": common_types.make_vector(common_types.StrId),
})

CBossSpawnGroupComponent = Object({
    **CSpawnGroupComponentFields,
    "sBossBattleLabel": common_types.StrId,
})

CLogicShapeComponent = Object(CLogicShapeComponentFields := {
    **CActorComponentFields,
    "pLogicShape": Pointer_game_logic_collision_CShape.create_construct(),
    "bWantsToGenerateNavMeshEdges": construct.Flag,
})

CBreakableHintComponent = Object(CLogicShapeComponentFields)

CBreakableScenarioComponent = Object({
    **CComponentFields,
    "aVignettes": common_types.make_vector(common_types.StrId),
})

CBreakableTileGroupComponent_STileInfo = Object({
    "eTileType": common_types.UInt,
    "vGridCoords": common_types.CVector2D,
    "sHiddenSG": common_types.StrId,
    "bIsHidingSecret": construct.Flag,
    "aVignettes": common_types.make_vector(common_types.StrId),
})

CBreakableTileGroupComponent = Object({
    **CSceneComponentFields,
    "uGroupId": common_types.UInt,
    "aGridTiles": common_types.make_vector(CBreakableTileGroupComponent_STileInfo),
    "bFakeHusks": construct.Flag,
    "eCollisionMaterial": common_types.UInt,
})

CSonarTargetComponent = Object(CSonarTargetComponentFields := CComponentFields)

CBreakableTileGroupSonarTargetComponent = Object(CSonarTargetComponentFields)

CBreakableVignetteComponent = Object({
    **CLogicShapeComponentFields,
    "sVignetteSG": common_types.StrId,
    "bUnhideWhenPlayerInside": construct.Flag,
    "bPreventVisibilityOnly": construct.Flag,
    "bForceNotVisible": construct.Flag,
})

CCameraComponent = Object({
    **CComponentFields,
    "fCurrentInterp": common_types.Float,
    "vCurrentPos": common_types.CVector3D,
    "vCurrentDir": common_types.CVector3D,
    "fDefaultInterp": common_types.Float,
    "fCurrentInterpChangeSpeed": common_types.Float,
    "fDefaultNear": common_types.Float,
    "fDefaultFar": common_types.Float,
    "bIgnoreSlomo": construct.Flag,
})

IPath = Object(IPathFields := {})

ISubPath = Object(ISubPathFields := {})

IPathNode = Object(IPathNodeFields := {})

SCameraRailNode = Object({
    **IPathNodeFields,
    "vPos": common_types.CVector3D,
    "wpLogicCamera": common_types.StrId,
})

SCameraSubRail = Object({
    **ISubPathFields,
    "tNodes": common_types.make_vector(SCameraRailNode),
})

SCameraRail = Object({
    **IPathFields,
    "tSubRails": common_types.make_vector(SCameraSubRail),
    "fMaxRailSpeed": common_types.Float,
    "fMinRailSpeed": common_types.Float,
    "fMaxRailDistance": common_types.Float,
})

CCameraRailComponent = Object({
    **CActorComponentFields,
    "oCameraRail": SCameraRail,
})

CElevatorUsableComponent = Object(CElevatorUsableComponentFields := {
    **CUsableComponentFields,
    "eDirection": common_types.UInt,
    "eLoadingScreen": common_types.UInt,
    "sLevelName": common_types.StrId,
    "sScenarioName": common_types.StrId,
    "sTargetSpawnPoint": common_types.StrId,
    "sMapConnectionId": common_types.StrId,
    "fMinTimeLoad": common_types.Float,
})

CCapsuleUsableComponent = Object({
    **CElevatorUsableComponentFields,
    "wpCapsule": common_types.StrId,
    "wpSkybase": common_types.StrId,
})

CCaterzillaAIComponent = Object(CBehaviorTreeAIComponentFields)

CCaterzillaSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "eSpawnDir": common_types.UInt,
    "eSpawnOrder": common_types.UInt,
    "NumCaterzillas": common_types.UInt,
    "fTimeToGenerateNextWave": common_types.Float,
    "wpSpawnPointLinked": common_types.StrId,
    "fTimeToRespawnAllCaterzillas": common_types.Float,
    "aHomeLandmarks": common_types.make_vector(common_types.StrId),
    "bInOutSpawnPoint": construct.Flag,
})

CCentralUnitComponent_SStartPointInfo = Object({
    "wpStartPoint": common_types.StrId,
    "wpEmmyLandmark": common_types.StrId,
})

CCentralUnitWeightedEdges = Object({
    "sId": common_types.StrId,
    "pLogicShape": common_types.StrId,
    "fFactorToAdd": common_types.Float,
    "fFactorToMultiply": common_types.Float,
})

CCentralUnitComponent = Object(CCentralUnitComponentFields := {
    **CActorComponentFields,
    "eMode": common_types.UInt,
    "bStartEnabled": construct.Flag,
    "wpBossSpawnPoint": common_types.StrId,
    "wpCentralUnitAI": common_types.StrId,
    "wpBossAlive": common_types.StrId,
    "wpBossDestroyed": common_types.StrId,
    "wpBossDoor": common_types.StrId,
    "sBossCollisionCameraID": common_types.StrId,
    "wpEmmySpawnPoint": common_types.StrId,
    "tEmmyStartPointsInfo": common_types.make_vector(CCentralUnitComponent_SStartPointInfo),
    "wpEmmyZoneShape": common_types.StrId,
    "wpDestroySearchLandmark": common_types.StrId,
    "tEmmyForbiddenShapes": common_types.make_vector(common_types.StrId),
    "tEmmyWeightedShapes": common_types.make_vector(Pointer_CCentralUnitWeightedEdges.create_construct()),
    "bUnlockDoorsOnEmmyDead": construct.Flag,
    "tEmmyLockedDoors": common_types.make_vector(common_types.StrId),
    "tEmmyPhase2DeactivatedActors": common_types.make_vector(common_types.StrId),
    "wpStartCombatCheckpointStartPoint": common_types.StrId,
    "sStartCombatCheckpointSnapshotId": common_types.StrId,
    "wpDeadCheckpointStartPoint": common_types.StrId,
})

CCaveCentralUnitComponent = Object({
    **CCentralUnitComponentFields,
    "wpGate": common_types.StrId,
})

CCentralUnitAIComponent = Object({
    **CBehaviorTreeAIComponentFields,
    "vSpawnPointActors": common_types.make_vector(common_types.StrId),
    "eType": common_types.UInt,
    "wpDoorCentralUnit": common_types.StrId,
    "wpDeadCutScenePlayer": common_types.StrId,
})

CCentralUnitCannonAIComponent = Object(CAIComponentFields)

CProjectileMovement = Object(CProjectileMovementFields := {
    **CWeaponMovementFields,
    "fMaxDist": common_types.Float,
    "fMaxLifeTime": common_types.Float,
    "sCollisionFX": common_types.StrId,
    "fFXAngZOffset": common_types.Float,
    "fFXScl": common_types.Float,
    "sNoDamageFX": common_types.StrId,
    "sEnergyCollisionFX": common_types.StrId,
})

CCentralUnitCannonBeamMovementComponent = Object(CProjectileMovementFields)

CChainReactionActionSwitcherComponent = Object(CComponentFields)

CChangeStageNavMeshItemComponent = Object(CComponentFields)

CCharacterMovement = Object(CCharacterMovementFields := CMovementComponentFields)

CChozoCommanderAIComponent = Object({
    **CBossAIComponentFields,
    "bUltimateGrabTestMode": construct.Flag,
    "wpUltimateGrabLandmark": common_types.StrId,
    "wpDeadCutScenePlayer": common_types.StrId,
    "wpPhase2CutscenePlayer": common_types.StrId,
    "wpPhase3CutscenePlayer": common_types.StrId,
    "wpPhase3EndLeftCutscenePlayer": common_types.StrId,
    "wpPhase3EndRightCutscenePlayer": common_types.StrId,
})

CChozoCommanderEnergyShardsFragmentMovementComponent = Object(CProjectileMovementFields)

CChozoCommanderEnergyShardsSphereMovementComponent = Object(CProjectileMovementFields)

CChozoCommanderSentenceSphereLifeComponent = Object(CBasicLifeComponentFields)

CChozoCommanderSentenceSphereMovementComponent = Object(CProjectileMovementFields)

CChozoCommanderXLifeComponent = Object({
    **CLifeComponentFields,
    "wpIntroductionCutScenePlayer": common_types.StrId,
    "wpDeathCutScenePlayer": common_types.StrId,
})

CChozoRobotSoldierAIComponent = Object({
    **CBossAIComponentFields,
    "bAlternativeSkin": construct.Flag,
    "wpPatrolPath": common_types.StrId,
    "tShootingPositions": common_types.make_vector(common_types.StrId),
})

CChozoRobotSoldierBeamMovementComponent = Object(CProjectileMovementFields)

CChozoWarriorAIComponent = Object(CChozoWarriorAIComponentFields := {
    **CBossAIComponentFields,
    "wpChozoWarrioXSpawnPoint": common_types.StrId,
    "eTransformationType": common_types.UInt,
})

CChozoWarriorEliteAIComponent = Object(CChozoWarriorAIComponentFields)

CChozoWarriorXAIComponent = Object(CChozoWarriorXAIComponentFields := CChozoWarriorAIComponentFields)

CChozoWarriorXEliteAIComponent = Object(CChozoWarriorXAIComponentFields)

CChozoWarriorXSpitMovementComponent = Object(CProjectileMovementFields)

CChozoZombieXAIComponent = Object(CBehaviorTreeAIComponentFields)

CChozoZombieXSpawnPointComponent = Object(CSpawnPointComponentFields)

CChozombieFXComponent = Object(CSceneComponentFields)

CTriggerLogicAction = Object(CTriggerLogicActionFields := {})

CTriggerComponent_SActivationCondition = Object({
    "sID": common_types.StrId,
    "sCharclasses": common_types.StrId,
    "bEnabled": construct.Flag,
    "bAlways": construct.Flag,
    "bDone": construct.Flag,
    "fExecutesEvery": common_types.Float,
    "fExecutesEveryRandomRange": common_types.Float,
    "fLastExecution": common_types.Float,
    "eEvent": common_types.UInt,
    "vLogicActions": common_types.make_vector(Pointer_CTriggerLogicAction.create_construct()),
})

CTriggerComponent = Object(CTriggerComponentFields := {
    **CComponentFields,
    "bCallEntityLuaCallback": construct.Flag,
    "iReverb": common_types.Int,
    "iLowPassFilter": common_types.Int,
    "sOnEnable": common_types.StrId,
    "sOnDisable": common_types.StrId,
    "bOnEnableAlways": construct.Flag,
    "bOnDisableAlways": construct.Flag,
    "bStartEnabled": construct.Flag,
    "bCheckAllEntities": construct.Flag,
    "bPersistentState": construct.Flag,
    "sSfxType": common_types.StrId,
    "lstActivationConditions": common_types.make_vector(Pointer_CTriggerComponent_SActivationCondition.create_construct()),
})

CColliderTriggerComponent = Object({
    **CTriggerComponentFields,
    "lnkShape": common_types.StrId,
})

CCollisionMaterialCacheComponent = Object(CComponentFields)

CConstantMovement = Object(CCharacterMovementFields)

CCooldownXBossAIComponent = Object({
    **CBossAIComponentFields,
    "wpWindTunnelDamageTrigger": common_types.StrId,
    "wpLavaCarpetFloorFX": common_types.StrId,
    "wpCoolShinesparkTrigger": common_types.StrId,
    "wpDeathCutscenePlayer": common_types.StrId,
    "wpDeathFromGrabCutscenePlayer": common_types.StrId,
})

CCooldownXBossFireBallMovementComponent = Object(CProjectileMovementFields)

CCooldownXBossWeakPointLifeComponent = Object(CBasicLifeComponentFields)

CCoreXAIComponent = Object(CBossAIComponentFields)

CCubeMapComponent = Object({
    **CComponentFields,
    "vCubePos": common_types.CVector3D,
    "fAttMin": common_types.Float,
    "fAttMax": common_types.Float,
    "vBoxBounds": common_types.CVector3D,
    "fIntensity": common_types.Float,
    "bEnableCulling": construct.Flag,
    "sTexturePathSpecular": common_types.StrId,
    "sTexturePathDiffuse": common_types.StrId,
})

CCutsceneComponent_SActorInfo = Object(CCutsceneComponent_SActorInfoFields := {
    "sId": common_types.StrId,
    "lnkActor": common_types.StrId,
    "bStartingVisibleState": construct.Flag,
    "bReceiveLogicUpdate": construct.Flag,
    "vctVisibilityPerTake": common_types.make_vector(construct.Flag),
})

CCutsceneComponent = Object({
    **CActorComponentFields,
    "sCutsceneName": common_types.StrId,
    "bDisableScenarioEntitiesOnPlay": construct.Flag,
    "vOriginalPos": common_types.CVector3D,
    "vctCutscenesOffsets": common_types.make_vector(common_types.CVector3D),
    "vctExtraInvolvedSubareas": common_types.make_vector(common_types.StrId),
    "vctExtraInvolvedActors": common_types.make_vector(CCutsceneComponent_SActorInfo),
    "vctOnBeforeCutsceneStartsLA": common_types.make_vector(Pointer_CTriggerLogicAction.create_construct()),
    "vctOnAfterCutsceneEndsLA": common_types.make_vector(Pointer_CTriggerLogicAction.create_construct()),
    "bHasSamusAsExtraActor": construct.Flag,
})

CCutsceneTriggerComponent = Object({
    **CBaseTriggerComponentFields,
    "lnkTargetCutsceneActor": common_types.StrId,
    "bOneShot": construct.Flag,
})

CSluggerAIComponent = Object(CSluggerAIComponentFields := CBehaviorTreeAIComponentFields)

CDaivoAIComponent = Object({
    **CSluggerAIComponentFields,
    "wpSwarmActor": common_types.StrId,
    "wpSwarmAOIBegin": common_types.StrId,
    "wpSwarmAOIEnd": common_types.StrId,
    "fChaseForcedDistanceToWall": common_types.Float,
})

CSwarmControllerComponent = Object(CSwarmControllerComponentFields := {
    **CComponentFields,
    "wpPathToFollow": common_types.StrId,
    "ePathType": common_types.UInt,
    "fGroupVelocity": common_types.Float,
})

CFlockingSwarmControllerComponent = Object(CFlockingSwarmControllerComponentFields := CSwarmControllerComponentFields)

CRedenkiSwarmControllerComponent = Object(CRedenkiSwarmControllerComponentFields := CFlockingSwarmControllerComponentFields)

CDaivoSwarmControllerComponent = Object(CRedenkiSwarmControllerComponentFields)

CDamageComponent = Object(CComponentFields)

CDamageTriggerConfig = Object({
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
})

CDamageTriggerComponent = Object({
    **CBaseDamageTriggerComponentFields,
    "oConfig": CDamageTriggerConfig,
})

CDemolitionBlockLifeComponent = Object(CDemolitionBlockLifeComponentFields := {
    **CLifeComponentFields,
    "wpOtherBlock": common_types.StrId,
})

CDemolitionBlockActivatableActorLifeComponent = Object({
    **CDemolitionBlockLifeComponentFields,
    "oActivatableObjController": common_types.StrId,
})

CDemolitionBlockComponent = Object({
    **CActivatableComponentFields,
    "vObjsToEnable": common_types.make_vector(common_types.StrId),
    "vObjsToDisable": common_types.make_vector(common_types.StrId),
})

CDemolitionBlockSonarTargetComponent = Object(CSonarTargetComponentFields)

CDirLightComponent = Object({
    **CBaseLightComponentFields,
    "vDir": common_types.CVector3D,
    "fAnimFrame": common_types.Float,
    "bCastShadows": construct.Flag,
})

CDizzeanSwarmControllerComponent = Object(CFlockingSwarmControllerComponentFields)

CDoorLifeComponent = Object(CDoorLifeComponentFields := {
    **CItemLifeComponentFields,
    "fMaxDistanceOpened": common_types.Float,
    "wpLeftDoorShieldEntity": common_types.StrId,
    "wpRightDoorShieldEntity": common_types.StrId,
    "fMinTimeOpened": common_types.Float,
    "bStayOpen": construct.Flag,
    "bStartOpened": construct.Flag,
    "bOnBlackOutOpened": construct.Flag,
    "bDoorIsWet": construct.Flag,
    "bFrozenDuringColdown": construct.Flag,
    "iAreaLeft": common_types.Int,
    "iAreaRight": common_types.Int,
    "aVignettes": common_types.make_vector(common_types.StrId),
    "sShieldEntity": common_types.StrId,
})

CDoorCentralUnitLifeComponent = Object({
    **CDoorLifeComponentFields,
    "eMode": common_types.UInt,
})

CDoorEmmyFXComponent = Object(CComponentFields)

CDoorGrapplePointComponent = Object(CPullableGrapplePointComponentFields)

CDredhedAIComponent = Object(CBehaviorTreeAIComponentFields)

CDredhedAttackComponent = Object(CAIAttackComponentFields)

CDropComponent = Object(CComponentFields)

CDroppableComponent = Object(CDroppableComponentFields := {
    **CComponentFields,
    "fMaxTimeAlive": common_types.Float,
})

CDroppableLifeComponent = Object({
    **CDroppableComponentFields,
    "fAmount": common_types.Float,
})

CDroppableMissileComponent = Object({
    **CDroppableComponentFields,
    "sItemMax": common_types.StrId,
    "sItemCurrent": common_types.StrId,
})

CDroppablePowerBombComponent = Object({
    **CDroppableComponentFields,
    "sItemMax": common_types.StrId,
    "sItemCurrent": common_types.StrId,
})

CDroppableSpecialEnergyComponent = Object({
    **CDroppableComponentFields,
    "fAmount": common_types.Float,
})

CDropterAIComponent = Object(CBehaviorTreeAIComponentFields)

CDummyAIComponent = Object(CAIComponentFields)

CDummyMovement = Object(CMovementComponentFields)

CDummyPullableGrapplePointComponent = Object(CPullableGrapplePointComponentFields)

CElectricGeneratorComponent = Object({
    **CUsableComponentFields,
    "eBlackOutZone": common_types.UInt,
    "sOnEnterUseLuaCallback": common_types.StrId,
    "vAffectedSubAreas": common_types.make_vector(common_types.StrId),
})

CElectricReactionComponent = Object(CElectricReactionComponentFields := CComponentFields)

CElectrifyingAreaComponent = Object({
    **CComponentFields,
    "bShouldUpdateAreaOnStart": construct.Flag,
})

CElevatorCommanderUsableComponent = Object({
    **CUsableComponentFields,
    "sTargetSpawnPoint": common_types.StrId,
})

CEmergencyLightElectricReactionComponent = Object(CElectricReactionComponentFields)

CEmmyOverrideDeathPositionDef = Object({
    "wpLandmark": common_types.StrId,
    "wpLogicShape": common_types.StrId,
})

CEmmyAutoForbiddenEdgesDef = Object({
    "wpCheckSamusLogicShape": common_types.StrId,
    "wpCheckEmmyLogicShape": common_types.StrId,
    "tForbiddenLogicShapes": common_types.make_vector(common_types.StrId),
    "tWeightedLogicShapeIDs": common_types.make_vector(common_types.StrId),
})

CEmmyAutoGlobalSmartLinkDef = Object({
    "wpStartLandmark": common_types.StrId,
    "tEndLandmarks": common_types.make_vector(common_types.StrId),
    "wpActivateLogicShape": common_types.StrId,
})

CEmmyAIComponent = Object(CEmmyAIComponentFields := {
    **CBehaviorTreeAIComponentFields,
    "sCurrentPatrol": common_types.StrId,
    "bPerceptionFeedbackEnabled": construct.Flag,
    "bShowBehaviorDebug": construct.Flag,
    "fPhaseDisplacementFactor": common_types.Float,
    "fGrabQTEFailTime": common_types.Float,
    "bPlayerNoiseEnabled": construct.Flag,
    "fPatrolSearchMaxTime": common_types.Float,
    "fGrabZoomOffset": common_types.Float,
    "fGrabZoomTime": common_types.Float,
    "bTargetDetectionEnabled": construct.Flag,
    "bTargetInsideEmmyZone": construct.Flag,
    "tOverrideGrabPosition": common_types.make_vector(Pointer_CEmmyOverrideDeathPositionDef.create_construct()),
    "tOverrideDeathPosition": common_types.make_vector(Pointer_CEmmyOverrideDeathPositionDef.create_construct()),
    "tAutoForbiddenEdges": common_types.make_vector(Pointer_CEmmyAutoForbiddenEdgesDef.create_construct()),
    "tAutoGlobalSmartLinks": common_types.make_vector(Pointer_CEmmyAutoGlobalSmartLinkDef.create_construct()),
    "tLogicShapesToAvoidCornerReposition": common_types.make_vector(common_types.StrId),
})

CEmmyAttackComponent = Object(CAIAttackComponentFields)

CEmmyCaveAIComponent = Object(CEmmyAIComponentFields)

CEmmyForestAIComponent = Object(CEmmyAIComponentFields)

CEmmyLabAIComponent = Object(CEmmyAIComponentFields)

CEmmyMagmaAIComponent = Object(CEmmyAIComponentFields)

CEnemyMovement = Object(CEnemyMovementFields := CCharacterMovementFields)

CEmmyMovement = Object(CEnemyMovementFields)

CEmmyProtoAIComponent = Object({
    **CEmmyAIComponentFields,
    "sDirtMaterialConstantId": common_types.StrId,
})

CEmmySancAIComponent = Object({
    **CEmmyAIComponentFields,
    "tFast4LegTransformationMagnet": common_types.make_vector(common_types.StrId),
    "wpForceEmmyPerceptionVisionConeOffShape": common_types.StrId,
    "bZipLine004Behavior": construct.Flag,
    "wpPhase2HeatEnabledLogicShape": common_types.StrId,
})

CEmmyShipyardAIComponent = Object(CEmmyAIComponentFields)

CEmmySpawnPointComponent = Object(CSpawnPointComponentFields)

CEmmyValveComponent = Object(CComponentFields)

CEventPropComponent = Object(CEventPropComponentFields := CComponentFields)

CEmmyWakeUpComponent = Object({
    **CEventPropComponentFields,
    "wpCentralUnit": common_types.StrId,
})

CEmmyWaveMovementComponent = Object(CProjectileMovementFields)

CEnhanceWeakSpotComponent = Object(CEnhanceWeakSpotComponentFields := CComponentFields)

CEscapeSequenceExplosionComponent = Object(CComponentFields)

CEvacuationCountDown = Object({
    **CEventPropComponentFields,
    "vEntitiesToPowerOff": common_types.make_vector(common_types.StrId),
})

CEventScenarioComponent = Object({
    **CComponentFields,
    "vEventActors": common_types.make_vector(common_types.StrId),
    "sIdleAction": common_types.StrId,
    "sReactionAction": common_types.StrId,
    "sFinishedAction": common_types.StrId,
    "sRecoveryAction": common_types.StrId,
    "bPersistent": construct.Flag,
    "bDisableOnXParasite": construct.Flag,
    "bDisableOnCoolDown": construct.Flag,
    "bReactOnFireOnly": construct.Flag,
    "bReactOnEnemies": construct.Flag,
    "bReactToSamus": construct.Flag,
    "bIgnoreSamusWithOC": construct.Flag,
    "bReactToSamusFiring": construct.Flag,
    "bReactToFireImpact": construct.Flag,
    "fTimeForRecoveryOnStay": common_types.Float,
    "fTimeForRecoveryOnExit": common_types.Float,
    "fInitRelaxFrame": common_types.Float,
})

CFXComponent = Object({
    **CSceneComponentFields,
    "fSelectedHighRadius": common_types.Float,
    "fSelectedLowRadius": common_types.Float,
})

CFactionComponent = Object(CComponentFields)

CFakePhysicsMovement = Object(CMovementComponentFields)

CFanComponent = Object({
    **CBaseTriggerComponentFields,
    "fWindLength": common_types.Float,
    "fHurricaneLength": common_types.Float,
    "fBarrierLength": common_types.Float,
    "fWidth": common_types.Float,
    "fParticleScale": common_types.Float,
})

CFanCoolDownComponent = Object(CComponentFields)

CFingSwarmControllerComponent = Object(CFlockingSwarmControllerComponentFields)

CFireComponent = Object(CComponentFields)

CFloatingPropActingComponent = Object(CComponentFields)

CShockWaveComponent = Object(CShockWaveComponentFields := CComponentFields)

CFloorShockWaveComponent = Object(CShockWaveComponentFields)

CFootstepPlatformComponent = Object({
    **CComponentFields,
    "wpActivableEntity": common_types.StrId,
    "wpPartnerFootStepPlatformEntity": common_types.StrId,
    "sCallbackOnOpened": common_types.StrId,
    "sCallbackOnClosed": common_types.StrId,
})

CForcedMovementAreaComponent = Object({
    **CActorComponentFields,
    "bForcedAreaOnce": construct.Flag,
    "eForcedDirection": common_types.UInt,
})

CFreezeRoomConfig = Object({
    "fActivationDelayTime": common_types.Float,
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
})

CFreezeRoomCoolConfig = Object({
    "fActivationDelayTime": common_types.Float,
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
})

CFreezeRoomComponent = Object({
    **CBaseDamageTriggerComponentFields,
    "oFreezeConfig": CFreezeRoomConfig,
    "oCoolConfig": CFreezeRoomCoolConfig,
    "sEnterZoneSound": common_types.StrId,
    "sVisualPresetOverride": common_types.StrId,
})

CFrozenComponent = Object(CFrozenComponentFields := CComponentFields)

CFrozenAsFrostbiteComponent = Object(CFrozenComponentFields)

CFrozenAsPlatformComponent = Object(CFrozenComponentFields)

CFrozenPlatformComponent = Object({
    **CComponentFields,
    "wpWeightPlatform": common_types.StrId,
})

CFulmiteBellyMineAIComponent = Object(CBehaviorTreeAIComponentFields)

CFulmiteBellyMineAttackComponent = Object(CAIAttackComponentFields)

CFulmiteBellyMineMovementComponent = Object(CProjectileMovementFields)

CFusibleBoxComponent = Object(CComponentFields)

CGobblerAIComponent = Object(CBehaviorTreeAIComponentFields)

CGobblerSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "wpDoor": common_types.StrId,
    "wpWeb": common_types.StrId,
})

CGoliathAIComponent = Object(CGoliathAIComponentFields := CBaseBigFistAIComponentFields)

CGoliathXAIComponent = Object({
    **CGoliathAIComponentFields,
    "wpCoreXSpawnPoint": common_types.StrId,
})

CGoliathXBurstProjectionBombMovement = Object(CBombMovementFields)

CGooplotAIComponent = Object(CGooplotAIComponentFields := CBehaviorTreeAIComponentFields)

CGooshockerAIComponent = Object(CGooplotAIComponentFields)

CGrabComponent = Object({
    **CComponentFields,
    "bIsInGrab": construct.Flag,
    "eLinkModeAsGrabber": common_types.UInt,
})

CGrappleBeamComponent = Object({
    **CWeaponMovementFields,
    "sIniFXId": common_types.StrId,
    "sEndFXId": common_types.StrId,
    "sGrappleFX": common_types.StrId,
})

CGroundShockerAIComponent = Object(CBaseGroundShockerAIComponentFields)

CGunComponent = Object(CGunComponentFields := CComponentFields)

CHangableGrappleSurfaceComponent = Object(CHangableGrappleSurfaceComponentFields := CGrapplePointComponentFields)

CHangableGrappleMagnetSlidingBlockComponent = Object(CHangableGrappleSurfaceComponentFields)

CHangableGrapplePointComponent = Object(CGrapplePointComponentFields)

CHeatRoomConfig = Object({
    "fActivationDelayTime": common_types.Float,
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
    "bActivationDelayTimeOnlyForFirstTime": construct.Flag,
})

CHeatRoomCoolConfig = Object({
    "fActivationDelayTime": common_types.Float,
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
    "bActivationDelayTimeOnlyForFirstTime": construct.Flag,
})

CHeatRoomComponent = Object({
    **CBaseDamageTriggerComponentFields,
    "oHeatConfig": CHeatRoomConfig,
    "oCoolConfig": CHeatRoomCoolConfig,
    "sEnterZoneSound": common_types.StrId,
    "sVisualPresetOverride": common_types.StrId,
    "pEnvironmentFXActor": common_types.StrId,
    "vEnvironmentFXActors": common_types.make_vector(common_types.StrId),
})

CHeatableShieldComponent = Object(CComponentFields)

CHeatableShieldEnhanceWeakSpotComponent = Object(CEnhanceWeakSpotComponentFields)

CHecathonAIComponent = Object({
    **CBehaviorTreeAIComponentFields,
    "wpPatrolPath": common_types.StrId,
    "ePatrolPathType": common_types.UInt,
    "wpHarassPath": common_types.StrId,
    "eHarassPathType": common_types.UInt,
    "fTimeToGoPatrol": common_types.Float,
    "fSpeed": common_types.Float,
    "bIsEating": construct.Flag,
    "bCanEat": construct.Flag,
    "fPatrolEatDuration": common_types.Float,
    "fPatrolEatCooldown": common_types.Float,
    "uMask": common_types.UInt,
})

CHecathonLifeComponent = Object(CEnemyLifeComponentFields)

CHecathonPlanktonFXComponent = Object({
    **CSceneComponentFields,
    "sModelResPath": common_types.StrId,
})

CHomingMovement = Object(CProjectileMovementFields)

CHydrogigaAIComponent = Object({
    **CBossAIComponentFields,
    "wpPresentationCutscenePlayer": common_types.StrId,
    "wpDeadCutScenePlayer": common_types.StrId,
})

CMagnetSlidingBlockComponent = Object(CMagnetSlidingBlockComponentFields := {
    **CComponentFields,
    "fTimePreparingToOpen": common_types.Float,
    "fTimeToCompleteMovementTowardsEnd": common_types.Float,
    "fTimeToCompleteMovementTowardsStart": common_types.Float,
    "bContinueMovingOnStopHang": construct.Flag,
    "wpRail": common_types.StrId,
    "wpDoorOpeningOnAnimatedCamera": common_types.StrId,
    "fTotalMetersToMoveY": common_types.Float,
    "fTimeToOpen": common_types.Float,
    "bAutoOpenAfterPreparing": construct.Flag,
})

CHydrogigaZiplineComponent = Object({
    **CMagnetSlidingBlockComponentFields,
    "lstLinkedMagnetSlidingBlocks": common_types.make_vector(common_types.StrId),
})

CHydrogigaZiplineRailComponent = Object({
    **CComponentFields,
    "lstAttachedZiplines": common_types.make_vector(common_types.StrId),
})

CHyperBeamBlockLifeComponent = Object(CItemLifeComponentFields)

CMissileMovement = Object(CMissileMovementFields := {
    **CProjectileMovementFields,
    "sTrailFX": common_types.StrId,
    "sBurstFX": common_types.StrId,
    "sIgnitionFX": common_types.StrId,
    "sSPRNoDamageFX": common_types.StrId,
})

CIceMissileMovement = Object(CMissileMovementFields)

CInfesterAIComponent = Object(CBehaviorTreeAIComponentFields)

CInfesterBallAIComponent = Object(CBehaviorTreeAIComponentFields)

CInfesterBallAttackComponent = Object(CAIAttackComponentFields)

CInfesterBallLifeComponent = Object(CEnemyLifeComponentFields)

CInfesterBallMovementComponent = Object(CProjectileMovementFields)

CInputComponent = Object({
    **CComponentFields,
    "bInputIgnored": construct.Flag,
})

CInterpolationComponent = Object(CComponentFields)

CInventoryComponent = Object(CComponentFields)

CKraidAIComponent = Object({
    **CBossAIComponentFields,
    "wpStage1ArenaShape": common_types.StrId,
    "wpStage2ArenaShape": common_types.StrId,
    "wpPhase2CutScenePlayer": common_types.StrId,
    "wpDeadCutScenePlayer": common_types.StrId,
    "wpDeadFromZiplineOrMBCutscenePlayer": common_types.StrId,
})

CKraidAcidBlobsMovementComponent = Object(CProjectileMovementFields)

CKraidBouncingCreaturesMovementComponent = Object(CProjectileMovementFields)

CKraidNailMovementComponent = Object(CProjectileMovementFields)

CKraidShockerSplashMovementComponent = Object(CProjectileMovementFields)

CMovablePlatformComponent = Object(CMovablePlatformComponentFields := CMovementComponentFields)

CKraidSpikeMovablePlatformComponent = Object(CMovablePlatformComponentFields)

CLandmarkComponent = Object({
    **CActorComponentFields,
    "sLandmarkID": common_types.StrId,
})

CLiquidPoolBaseComponent = Object(CLiquidPoolBaseComponentFields := {
    **CBaseDamageTriggerComponentFields,
    "sModelPath": common_types.StrId,
    "eLowPassFilter": common_types.UInt,
    "eReverb": common_types.UInt,
})

CLavaPoolConfig = Object({
    "fDamagePerTime": common_types.Float,
    "fInBetweenDamageTime": common_types.Float,
    "fInitTimeDamageIncrease": common_types.Float,
    "fDamageIncreaseAmount": common_types.Float,
    "fMaxDamage": common_types.Float,
})

CLavaPoolComponent = Object({
    **CLiquidPoolBaseComponentFields,
    "oConfig": CLavaPoolConfig,
    "fChangeTime": common_types.Float,
})

CLavaPumpComponent = Object(CActivatableComponentFields)

CThermalReactionComponent = Object(CThermalReactionComponentFields := CComponentFields)

CLavapumpThermalReactionComponent = Object(CThermalReactionComponentFields)

CLifeRechargeComponent = Object({
    **CUsableComponentFields,
    "sRechargeFX": common_types.StrId,
    "sEyeRFX": common_types.StrId,
    "sEyeLFX": common_types.StrId,
})

CLightingComponent = Object(CComponentFields)

CLineBombMovement = Object(CBombMovementFields)

CLiquidSimulationComponent = Object(CComponentFields)

CLockOnMissileMovement = Object(CMissileMovementFields)

CLogicActionTriggerComponent = Object({
    **CComponentFields,
    "vLogicActions": common_types.make_vector(Pointer_CTriggerLogicAction.create_construct()),
})

CLogicCamera = Object({
    **CGameObjectFields,
    "sID": common_types.StrId,
    "sControllerID": common_types.StrId,
    "bStatic": construct.Flag,
    "v3Position": common_types.CVector3D,
    "v3Dir": common_types.CVector3D,
    "fFovX": common_types.Float,
    "fMinExtraZDist": common_types.Float,
    "fMaxExtraZDist": common_types.Float,
    "fDefaultInterp": common_types.Float,
})

CLogicCameraComponent = Object({
    **CActorComponentFields,
    "rLogicCamera": Pointer_CLogicCamera.create_construct(),
})

CLogicLookAtPlayerComponent = Object(CComponentFields)

SLogicPathNode = Object({
    **IPathNodeFields,
    "vPos": common_types.CVector3D,
    "fSwarmRadius": common_types.Float,
    "fDiversionChance": common_types.Float,
})

SLogicSubPath = Object({
    **ISubPathFields,
    "tNodes": common_types.make_vector(SLogicPathNode),
})

SLogicPath = Object({
    **IPathFields,
    "tSubPaths": common_types.make_vector(SLogicSubPath),
})

CLogicPathComponent = Object({
    **CActorComponentFields,
    "logicPath": SLogicPath,
})

CLogicPathNavMeshItemComponent = Object(CNavMeshItemComponentFields)

CMagmaCentralUnitComponent = Object({
    **CCentralUnitComponentFields,
    "wpGate": common_types.StrId,
})

CMagmaKraidPistonPlatformComponent = Object(CComponentFields)

CMagmaKraidScenarioControllerComponent = Object({
    **CComponentFields,
    "wpBackGorundPipesEntity": common_types.StrId,
    "wpPistonEntity": common_types.StrId,
})

CMagmaKraidSpikeComponent = Object(CComponentFields)

CMagnetMovablePlatformComponent = Object(CMagnetMovablePlatformComponentFields := CMovablePlatformComponentFields)

CMagnetSlidingBlockCounterWeightMovablePlatformComponent = Object({
    **CMagnetMovablePlatformComponentFields,
    "wpReferenceEntity": common_types.StrId,
})

CMagnetSlidingBlockRailComponent = Object(CComponentFields)

CMagnetSlidingBlockWithCollisionsComponent = Object(CMagnetSlidingBlockComponentFields)

CMagnetSurfaceComponent = Object(CActorComponentFields)

CMagnetSurfaceHuskComponent = Object(CComponentFields)

CMapAcquisitionComponent = Object({
    **CUsableComponentFields,
    "sLiteralID": common_types.StrId,
})

CMassiveCaterzillaSpawnGroupComponent = Object({
    **CSpawnGroupComponentFields,
    "fTimeToSpawn": common_types.Float,
    "fTimeToSpawnAfterDespawn": common_types.Float,
    "iNumCaterzillas": common_types.Int,
})

CMaterialFXComponent = Object(CSceneComponentFields)

CMeleeComponent = Object({
    **CComponentFields,
    "sBlockSyncFX": common_types.StrId,
})

CMenuAnimationChangeComponent = Object(CComponentFields)

CModelInstanceComponent = Object({
    **CSceneComponentFields,
    "sModelPath": common_types.StrId,
    "vScale": common_types.CVector3D,
})

CModelUpdaterComponent = Object(CModelUpdaterComponentFields := {
    **CSceneComponentFields,
    "sDefaultModelPath": common_types.StrId,
})

CMorphBallLauncherComponent = Object({
    **CComponentFields,
    "wpLauncherExit": common_types.StrId,
    "sTravellingAction": common_types.StrId,
    "bManualActivation": construct.Flag,
})

CMorphBallLauncherExitComponent = Object({
    **CComponentFields,
    "vExpelDirection": common_types.CVector2D,
    "fExpelImpulseSize": common_types.Float,
    "fInputIgnoreTimeAfterExpelling": common_types.Float,
    "fFrictionIgnoreTimeAfterExpelling": common_types.Float,
    "bWantsRelocationAndExpelImpulse": construct.Flag,
    "bWantsAutomaticOpenOnStartLaunchProcess": construct.Flag,
})

CPlayerMovement = Object(CPlayerMovementFields := {
    **CCharacterMovementFields,
    "bForcedAnalogInput": construct.Flag,
    "fImpactImpulseX": common_types.Float,
    "fImpactImpulseY": common_types.Float,
    "fImpactAirImpulseY": common_types.Float,
    "fImpactHardImpulseX": common_types.Float,
    "fImpactHardImpulseY": common_types.Float,
    "fImpactHardAirImpulseY": common_types.Float,
})

CMorphBallMovement = Object({
    **CPlayerMovementFields,
    "bIsMorphBall": construct.Flag,
    "bIsSamus": construct.Flag,
    "fRunningSpeedX": common_types.Float,
    "fSpiderRunningSpeedX": common_types.Float,
    "fSpiderImpulseSpeedX": common_types.Float,
    "fAirRunningSpeedX": common_types.Float,
    "fSpeedY": common_types.Float,
    "fHighJumpBootSpeedY": common_types.Float,
    "fMinSpeedY": common_types.Float,
    "fMaxSpeedY": common_types.Float,
    "fTimeOnAirAllowingJump": common_types.Float,
    "fNoJumpingGravityFactor": common_types.Float,
    "fImpactIgnoreInputTime": common_types.Float,
    "fImpactIgnoreFrictionTime": common_types.Float,
    "sMovingFX": common_types.StrId,
    "sMovingOilFX": common_types.StrId,
    "sMovingOilSlidingFX": common_types.StrId,
    "sTransformationCustomMaterialFX": common_types.StrId,
    "sTransformationParticlesFX": common_types.StrId,
    "sImpulseFX": common_types.StrId,
    "sFallDustFX": common_types.StrId,
    "sFallOilFX": common_types.StrId,
    "fMinTimeInOilState": common_types.Float,
    "fTotalTimeIgnoringGoToSpider": common_types.Float,
    "sSpiderImpulseEndShake": common_types.StrId,
})

CMovableGrapplePointComponent = Object(CPullableGrapplePointComponentFields)

CMultiLockOnBlockComponent = Object({
    **CComponentFields,
    "vMultiLockOnPoints": common_types.make_vector(common_types.StrId),
})

CMultiLockOnPointComponent = Object({
    **CActivatableByProjectileComponentFields,
    "wpMultiLockOnBlock": common_types.StrId,
})

CMultiModelUpdaterComponent = Object(CMultiModelUpdaterComponentFields := {
    **CModelUpdaterComponentFields,
    "sModelAlias": common_types.StrId,
})

CMushroomPlatformComponent = Object({
    **CLifeComponentFields,
    "fAlertTimeToRetract": common_types.Float,
    "fRetractedTimeToRelax": common_types.Float,
})

CNailongAIComponent = Object({
    **CBehaviorTreeAIComponentFields,
    "wpPatrolPath": common_types.StrId,
    "ePatrolPathType": common_types.UInt,
})

CNailongThornMovementComponent = Object(CProjectileMovementFields)

CNailuggerAcidBallMovementComponent = Object(CProjectileMovementFields)

CNoFreezeRoomComponent = Object(CLogicShapeComponentFields)

CObsydomithonAIComponent = Object(CBehaviorTreeAIComponentFields)

COmniLightComponent = Object({
    **CBaseLightComponentFields,
    "fAttMin": common_types.Float,
    "fAttMax": common_types.Float,
    "fAttConstantFactor": common_types.Float,
    "fAttQuadraticFactor": common_types.Float,
    "bCastShadows": construct.Flag,
    "bStaticShadows": construct.Flag,
    "fShadowScl": common_types.Float,
})

CPerceptionComponent = Object(CComponentFields)

CPersistenceComponent = Object(CComponentFields)

CPickableComponent = Object(CPickableComponentFields := {
    **CComponentFields,
    "sOnPickFX": common_types.StrId,
})

CPickableItemComponent = Object(CPickableItemComponentFields := {
    **CPickableComponentFields,
    "sBTType": common_types.StrId,
    "sBTHiddenSceneGroup": common_types.StrId,
    "fTimeToCanBePicked": common_types.Float,
    "sStartPoint": common_types.StrId,
})

CPickableSpringBallComponent = Object(CPickableItemComponentFields)

CPickableSuitComponent = Object(CPickableItemComponentFields)

CPlatformTrapGrapplePointComponent = Object(CPullableGrapplePointComponentFields)

CPlayerLifeComponent = Object({
    **CCharacterLifeComponentFields,
    "fImpactInvulnerableTime": common_types.Float,
    "sImpactHardAnim": common_types.StrId,
    "sHardImpactFX": common_types.StrId,
    "fLifeShards": common_types.Float,
})

CPoisonFlyAIComponent = Object(CBehaviorTreeAIComponentFields)

base_global_CFilePathStrId = common_types.StrId

CPositionalSoundComponent = Object({
    **CComponentFields,
    "fMinAtt": common_types.Float,
    "fMaxAtt": common_types.Float,
    "fVol": common_types.Float,
    "fPitch": common_types.Float,
    "fLaunchEvery": common_types.Float,
    "fHorizontalMult": common_types.Float,
    "fVerticalMult": common_types.Float,
    "bLoop": construct.Flag,
    "fFadeInTime": common_types.Float,
    "fFadeOutTime": common_types.Float,
    "sSound1": Pointer_base_global_CFilePathStrId.create_construct(),
    "sSound2": Pointer_base_global_CFilePathStrId.create_construct(),
    "sSound3": Pointer_base_global_CFilePathStrId.create_construct(),
    "sSound4": Pointer_base_global_CFilePathStrId.create_construct(),
})

CPowerBombBlockLifeComponent = Object(CLifeComponentFields)

CPowerBombMovement = Object({
    **CBombMovementFields,
    "fRadiusToAlertMorphball": common_types.Float,
})

CPowerGeneratorComponent = Object({
    **CActivatableComponentFields,
    "wpPowerGeneratorUsable": common_types.StrId,
    "wpPowerGeneratorUsablePlatform": common_types.StrId,
})

CPowerUpLifeComponent = Object({
    **CItemLifeComponentFields,
    "wpCheckPointEntity": common_types.StrId,
    "sPowerupNameLabelID": common_types.StrId,
})

CProfessorDoorComponent = Object(CEventPropComponentFields)

CProtoCentralUnitComponent = Object({
    **CCentralUnitComponentFields,
    "wpGate": common_types.StrId,
})

CProtoEmmyChaseMusicTriggerComponent = Object(CBaseTriggerComponentFields)

CPullOffGrapplePointComponent = Object({
    **CPullableGrapplePointComponentFields,
    "oActivatableObj": common_types.StrId,
})

CQuarentineDoorComponent = Object(CEventPropComponentFields)

CQuetzoaAIComponent = Object(CQuetzoaAIComponentFields := {
    **CBossAIComponentFields,
    "wpShortRangePath": common_types.StrId,
    "eShortRangePathType": common_types.UInt,
    "wpLongRangePath": common_types.StrId,
    "eLongRangePathType": common_types.UInt,
})

CQuetzoaEnergyWaveMovementComponent = Object(CProjectileMovementFields)

CQuetzoaMultiTargetProjectileMovementComponent = Object(CProjectileMovementFields)

CQuetzoaXAIComponent = Object({
    **CQuetzoaAIComponentFields,
    "wpCoreXSpawnPoint": common_types.StrId,
})

CSmartObjectComponent = Object(CSmartObjectComponentFields := {
    **CComponentFields,
    "sOnUseStart": common_types.StrId,
    "sOnUseFailure": common_types.StrId,
    "sOnUseSuccess": common_types.StrId,
    "sUsableEntity": common_types.StrId,
    "sDefaultUseAction": common_types.StrId,
    "sDefaultAbortAction": common_types.StrId,
    "bStartEnabled": construct.Flag,
    "fInterpolationTime": common_types.Float,
})

CReturnAreaSmartObjectComponent = Object(CSmartObjectComponentFields)

CRinkaAIComponent = Object(CAIComponentFields)

CRinkaUnitComponent = Object({
    **CComponentFields,
    "eRinkaType": common_types.UInt,
})

CRockDiverAIComponent = Object(CBehaviorTreeAIComponentFields)

CRockDiverSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "fTimeToSpawn": common_types.Float,
})

CRodotukAIComponent = Object(CRodotukAIComponentFields := {
    **CBehaviorTreeAIComponentFields,
    "eType": common_types.UInt,
})

CRodomithonXAIComponent = Object({
    **CRodotukAIComponentFields,
    "eFirePillarType": common_types.UInt,
})

CRotationalPlatformComponent = Object({
    **CComponentFields,
    "wpDestructibleBlock": common_types.StrId,
    "eRotationDirection": common_types.UInt,
})

CRumbleComponent = Object(CComponentFields)

CSabotoruAIComponent = Object({
    **CBehaviorTreeAIComponentFields,
    "fMinTimeBetweenSearch": common_types.Float,
    "fMaxTimeBetweenSearch": common_types.Float,
    "fMinTimeSearching": common_types.Float,
    "fMaxTimeSearching": common_types.Float,
})

CSabotoruLifeComponent = Object(CEnemyLifeComponentFields)

CSabotoruSpawnPointComponent = Object({
    **CSpawnPointComponentFields,
    "wpDoor": common_types.StrId,
    "wpHomeLandmark": common_types.StrId,
    "bRightSideDoor": construct.Flag,
})

CSamusAlternativeActionPlayerComponent = Object(CAlternativeActionPlayerComponentFields)

CSamusAnimationComponent = Object(CAnimationComponentFields)

CSamusGunComponent = Object({
    **CGunComponentFields,
    "sSpinAttackFX": common_types.StrId,
    "sScrewAttackFX": common_types.StrId,
})

CSamusModelUpdaterComponent = Object(CMultiModelUpdaterComponentFields)

CSamusMovement = Object({
    **CPlayerMovementFields,
    "bIsMorphBall": construct.Flag,
    "bIsSamus": construct.Flag,
    "fFixedModelOffsetYGoingUp": common_types.Float,
    "fFixedModelOffsetYGoingDown": common_types.Float,
    "fFixedRightLegSwivelAngleOffsetGoingUp": common_types.Float,
    "fFixedLeftLegSwivelAngleOffsetGoingUp": common_types.Float,
    "fFixedRightLegSwivelAngleOffsetGoingDown": common_types.Float,
    "fFixedLeftLegSwivelAngleOffsetGoingDown": common_types.Float,
    "fFixedRightLegOffsetGoingUp": common_types.CVector3D,
    "fFixedLeftLegOffsetGoingUp": common_types.CVector3D,
    "fFixedRightLegOffsetGoingDown": common_types.CVector3D,
    "fFixedLeftLegOffsetGoingDown": common_types.CVector3D,
    "fModelOffsetYGoingUp": common_types.Float,
    "fModelOffsetYGoingDown": common_types.Float,
    "fRightLegSwivelAngleOffsetGoingUp": common_types.Float,
    "fLeftLegSwivelAngleOffsetGoingUp": common_types.Float,
    "fRightLegSwivelAngleOffsetGoingDown": common_types.Float,
    "fLeftLegSwivelAngleOffsetGoingDown": common_types.Float,
    "fRightLegOffsetGoingUp": common_types.CVector3D,
    "fLeftLegOffsetGoingUp": common_types.CVector3D,
    "fRightLegOffsetGoingDown": common_types.CVector3D,
    "fLeftLegOffsetGoingDown": common_types.CVector3D,
    "s_fModelOffsetRunningYGoingUp": common_types.Float,
    "s_fModelOffsetRunningYGoingDown": common_types.Float,
    "s_fModelOffsetRunningYOCGoingUp": common_types.Float,
    "s_fModelOffsetRunningYOCGoingDown": common_types.Float,
    "s_fModelOffsetRunningYSlowDownGoingUp": common_types.Float,
    "s_fModelOffsetRunningYSlowDownGoingDown": common_types.Float,
})

CSaveStationUsableComponent = Object(CUsableComponentFields)

CSceneModelAnimationComponent = Object({
    **CComponentFields,
    "sModelAnim": common_types.StrId,
})

CSclawkAIComponent = Object(CSclawkAIComponentFields := CBehaviorTreeAIComponentFields)

CSclawkLifeComponent = Object(CEnemyLifeComponentFields)

CScorpiusAIComponent = Object({
    **CBossAIComponentFields,
    "wpPhase2CutScenePlayer": common_types.StrId,
    "wpPhase3CutScenePlayer": common_types.StrId,
    "wpDeadCutScenePlayer": common_types.StrId,
})

CScorpiusFXComponent = Object(CSceneComponentFields)

CScorpiusPoisonousSpitMovementComponent = Object(CProjectileMovementFields)

CScourgeAIComponent = Object(CBehaviorTreeAIComponentFields)

CScourgeLifeComponent = Object(CEnemyLifeComponentFields)

CScriptComponent = Object(CComponentFields)

CSegmentLightComponent = Object({
    **CBaseLightComponentFields,
    "vDir": common_types.CVector3D,
    "fSegmentLength": common_types.Float,
    "fAttMin": common_types.Float,
    "fAttMax": common_types.Float,
    "fAttConstantFactor": common_types.Float,
    "fAttQuadraticFactor": common_types.Float,
})

CSensorDoorComponent = Object(CComponentFields)

CShakernautAIComponent = Object(CRobotAIComponentFields)

CShelmitAIComponent = Object({
    **CBehaviorTreeAIComponentFields,
    "eShellState": common_types.UInt,
})

CShineonAIComponent = Object(CBehaviorTreeAIComponentFields)

CShipRechargeComponent = Object(CUsableComponentFields)

CShockWavePoolComponent = Object(CComponentFields)

SActivatabledOnEventInfo = Object({
    "pActivatable": common_types.StrId,
    "sIdActivation": common_types.StrId,
})

CShootActivatorComponent = Object(CShootActivatorComponentFields := {
    **CItemLifeComponentFields,
    "fInitialAccumulatedTime": common_types.Float,
    "fActivationTime": common_types.Float,
    "fTimePerShot": common_types.Float,
    "vTargetsToActivate": common_types.make_vector(common_types.StrId),
    "vTargetsToDeactivate": common_types.make_vector(common_types.StrId),
    "sOnUseEntityTimeline": common_types.StrId,
    "wpAtmosphereEntity": common_types.StrId,
    "vEntitiesActivatabledOnEvent": common_types.make_vector(SActivatabledOnEventInfo),
    "vEntitiesDeactivatabledOnEvent": common_types.make_vector(SActivatabledOnEventInfo),
})

CShootActivatorHidrogigaComponent = Object({
    **CShootActivatorComponentFields,
    "wpOtherActivator": common_types.StrId,
    "wpWaterNozzle": common_types.StrId,
})

CShotComponent = Object(CComponentFields)

CSideEnemyMovement = Object({
    **CEnemyMovementFields,
    "eInitialDir": common_types.UInt,
})

CSlidleSpawnPointComponent = Object({
    **CComponentFields,
    "eDespawnDir": common_types.UInt,
})

CSlowNailongSpawnPointComponent = Object(CSpawnPointComponentFields)

CSluggerAcidBallMovementComponent = Object(CProjectileMovementFields)

CSoundListenerComponent = Object({
    **CComponentFields,
    "vLookAt": common_types.CVector3D,
})

CSoundProofTriggerComponent = Object({
    **CBaseTriggerComponentFields,
    "eLowPassFilterToApply": common_types.UInt,
    "fFadeInTime": common_types.Float,
    "fFadeOutTime": common_types.Float,
    "bMuteActors": construct.Flag,
    "bFilterSpecificActors": construct.Flag,
    "vActorsToIgnore": common_types.make_vector(common_types.StrId),
})

CSpbSprActivator = Object({
    **CActivatableByProjectileComponentFields,
    "wpSpbSprpPlatform": common_types.StrId,
    "vTargetsToActivate": common_types.make_vector(common_types.StrId),
    "vTargetsToDeactivate": common_types.make_vector(common_types.StrId),
    "wpPoolPlatform": common_types.StrId,
})

CSpecialEnergyComponent = Object({
    **CComponentFields,
    "fMaxEnergy": common_types.Float,
    "fEnergy": common_types.Float,
    "bSpecialEnergyLocked": construct.Flag,
})

CSpitclawkAIComponent = Object(CSclawkAIComponentFields)

CVulkranMagmaBallMovementComponent = Object(CVulkranMagmaBallMovementComponentFields := CProjectileMovementFields)

CSpittailMagmaBallMovementComponent = Object(CVulkranMagmaBallMovementComponentFields)

CSpotLightComponent = Object({
    **CBaseLightComponentFields,
    "fAttMin": common_types.Float,
    "fAttMax": common_types.Float,
    "fAttIn": common_types.Float,
    "fAttOut": common_types.Float,
    "fAttConstantFactor": common_types.Float,
    "fAttQuadraticFactor": common_types.Float,
    "vDir": common_types.CVector3D,
    "fAnimFrame": common_types.Float,
    "bCastShadows": construct.Flag,
    "vShadowNearFar": common_types.CVector2D,
    "fShadowBias": common_types.Float,
    "bStaticShadows": construct.Flag,
    "fShadowScl": common_types.Float,
    "bHasProjectorTexture": construct.Flag,
    "sTexturePath": common_types.StrId,
    "vProjectorUVScroll": common_types.CVector4D,
})

SFXInstanceData = Object({
    "sFXPath": common_types.StrId,
    "v3Position": common_types.CVector3D,
    "v3Rotation": common_types.CVector3D,
    "v3Scale": common_types.CVector3D,
})

CStandaloneFXComponent = Object({
    **CSceneComponentFields,
    "vctFXInstances": common_types.make_vector(SFXInstanceData),
    "uPoolSize": common_types.UInt,
    "vScale": common_types.CVector3D,
    "sFXPath": common_types.StrId,
})

CStartPointComponent = Object({
    **CComponentFields,
    "sOnTeleport": common_types.StrId,
    "sOnTeleportLogicCamera": common_types.StrId,
    "bOnTeleportLogicCameraRaw": construct.Flag,
    "bProjectOnFloor": construct.Flag,
    "bMorphballMode": construct.Flag,
    "bSaveGameToCheckpoint": construct.Flag,
    "bIsBossStartPoint": construct.Flag,
})

CSteamJetComponent = Object({
    **CBaseDamageTriggerComponentFields,
    "fDelayStart": common_types.Float,
    "fDamage": common_types.Float,
    "fLength": common_types.Float,
    "fWidth": common_types.Float,
    "fOnTime": common_types.Float,
    "fOffTime": common_types.Float,
    "fOnOffTime": common_types.Float,
    "fParticleScale": common_types.Float,
    "bCrossingAllowed": construct.Flag,
    "bForceReactionDirection": construct.Flag,
    "vReactionDirection": common_types.CVector2D,
    "wpNextSteamJet": common_types.StrId,
})

CSteeringMovement = Object(CMovementComponentFields)

CSunnapAIComponent = Object(CRodotukAIComponentFields)

CSuperMissileMovement = Object(CMissileMovementFields)

CSwarmAttackComponent = Object(CAttackComponentFields)

CSwifterAIComponent = Object(CBehaviorTreeAIComponentFields)

CSwifterSpawnGroupComponent = Object({
    **CSpawnGroupComponentFields,
    "eDirection": common_types.UInt,
    "eMode": common_types.UInt,
    "fTimeToSpawn": common_types.Float,
})

CSwingableGrapplePointComponent = Object(CGrapplePointComponentFields)

CTakumakuAIComponent = Object(CBehaviorTreeAIComponentFields)

CTargetComponent = Object(CComponentFields)

CTeleporterUsableComponent = Object({
    **CUsableComponentFields,
    "eLoadingScreen": common_types.UInt,
    "sLevelName": common_types.StrId,
    "sScenarioName": common_types.StrId,
    "sTargetSpawnPoint": common_types.StrId,
    "eTeleporterColorSphere": common_types.UInt,
    "wpFrozenPlatform": common_types.StrId,
})

SDoorInfo = Object({
    "wpThermalDoor": common_types.StrId,
    "sDoorState": common_types.UInt,
})

CThermalDeviceComponent = Object({
    **CUsableComponentFields,
    "vThermalDoors": common_types.make_vector(SDoorInfo),
    "sOnEnterUseLuaCallback": common_types.StrId,
    "sOnSetupInitialStateLuaCallback": common_types.StrId,
    "sOnSetupUseStateLuaCallback": common_types.StrId,
    "sUseEndActionOverride": common_types.StrId,
    "bCheckpointBeforeUsage": construct.Flag,
    "ePipeGroup1": common_types.UInt,
    "ePipeGroup2": common_types.UInt,
})

CThermalRoomConnectionFX = Object({
    **CActivatableComponentFields,
    "vTargetToLink": common_types.StrId,
    "vHidderLink": common_types.StrId,
})

CThermalRoomFX = Object(CActivatableComponentFields)

CTimelineComponent = Object({
    **CComponentFields,
    "sInitAction": common_types.StrId,
    "eNextPolicy": common_types.UInt,
    "fMinDelayTime": common_types.Float,
    "fMaxDelayTime": common_types.Float,
})

CTimerComponent = Object(CComponentFields)

CTotalRechargeComponent = Object({
    **CUsableComponentFields,
    "sRechargeFX": common_types.StrId,
    "sEyeRFX": common_types.StrId,
    "sEyeLFX": common_types.StrId,
})

CTrainUsableComponent = Object(CTrainUsableComponentFields := {
    **CUsableComponentFields,
    "eDirection": common_types.UInt,
    "eLoadingScreen": common_types.UInt,
    "sLevelName": common_types.StrId,
    "sScenarioName": common_types.StrId,
    "sTargetSpawnPoint": common_types.StrId,
    "sMapConnectionId": common_types.StrId,
    "bAquaLoadingScreen": construct.Flag,
})

CTrainUsableComponentCutScene = Object({
    **CTrainUsableComponentFields,
    "wpCutScenePlayer": common_types.StrId,
})

CTrainWithPortalUsableComponent = Object({
    **CTrainUsableComponentFields,
    "wpPortal": common_types.StrId,
})

CTriggerNavMeshItemComponent = Object(CNavMeshItemComponentFields)

CTunnelTrapMorphballComponent = Object({
    **CComponentFields,
    "aVignettes": common_types.make_vector(common_types.StrId),
    "bDisableCloseTrapSensor": construct.Flag,
})

CUnlockAreaSmartObjectComponent = Object(CSmartObjectComponentFields)

CVideoManagerComponent = Object({
    **CComponentFields,
    "sVideo_1_Path": common_types.StrId,
    "sVideo_2_Path": common_types.StrId,
    "sVideoAux_1_Path": common_types.StrId,
    "sVideoAux_2_Path": common_types.StrId,
})

CVulkranAIComponent = Object(CBehaviorTreeAIComponentFields)

CWarLotusAIComponent = Object(CBehaviorTreeAIComponentFields)

CWaterNozzleComponent = Object({
    **CComponentFields,
    "wpWaterPool": common_types.StrId,
})

CWaterPlatformUsableComponent = Object({
    **CUsableComponentFields,
    "fTotalMetersToFill": common_types.Float,
    "fSnapToMeters": common_types.Float,
    "fMetersToBreakValve": common_types.Float,
    "fTimeToBreakValve": common_types.Float,
    "fTimeToFillAfterValveBreaks": common_types.Float,
    "fPlatformMovementDelaySinceUseStart": common_types.Float,
})

CWaterPoolComponent_FloatingEntitiesInfo = Object({
    "wpFloatingEntity": common_types.StrId,
    "fLevelStopFloating": common_types.Float,
})

CWaterPoolComponent = Object({
    **CLiquidPoolBaseComponentFields,
    "vWaterLevelChanges": common_types.make_vector(common_types.Float),
    "tFloatingEntities": common_types.make_vector(CWaterPoolComponent_FloatingEntitiesInfo),
    "sOnActivatedLuaCallback": common_types.StrId,
    "bChangedLevelOnCooldownEvent": construct.Flag,
    "vFloatingEntities": common_types.make_vector(common_types.StrId),
})

CWaterTriggerChangeComponent = Object({
    **CComponentFields,
    "wpOriginWaterTrigger": common_types.StrId,
    "wpTargetWaterTrigger": common_types.StrId,
    "fChangeTime": common_types.Float,
    "fDelay": common_types.Float,
    "bDeactivateOnFinished": construct.Flag,
    "wpOtherWaterTriggerChange": common_types.StrId,
    "fOriginChange": common_types.Float,
    "fTargetChange": common_types.Float,
    "sOnActivatedLuaCallback": common_types.StrId,
})

CWeightActivableMovablePlatformComponent = Object({
    **CMovablePlatformComponentFields,
    "sOnActivatedLuaCallback": common_types.StrId,
})

CWeightActivablePropComponent = Object(CComponentFields)

CWeightActivatedPlatformSmartObjectComponent = Object({
    **CSmartObjectComponentFields,
    "sDustFX": common_types.StrId,
    "bDisableWhenEmmyNearby": construct.Flag,
    "bDisableWhenUsed": construct.Flag,
})

SWorldGraphNode = Object({
    "vPos": common_types.CVector3D,
    "sID": common_types.StrId,
    "bDeadEnd": construct.Flag,
    "tNeighboursIds": common_types.make_vector(common_types.StrId),
})

CWorldGraph = Object({
    **CActorComponentFields,
    "tNodes": common_types.make_vector(SWorldGraphNode),
})

CXParasiteAIComponent = Object(CBehaviorTreeAIComponentFields)

CXParasiteBehavior = Object(CXParasiteBehaviorFields := {
    "bCanBeAbsorbed": construct.Flag,
    "fBehaviorProbability": common_types.Float,
    "fOverrideGreenTypeProbability": common_types.Float,
    "fOverrideYellowTypeProbability": common_types.Float,
    "fOverrideOrangeTypeProbability": common_types.Float,
    "fOverrideRedTypeProbability": common_types.Float,
})

CXParasiteDropComponent = Object({
    **CComponentFields,
    "vectBehaviors": common_types.make_vector(Pointer_CXParasiteBehavior.create_construct()),
})

CYamplotXAIComponent = Object(CBehaviorTreeAIComponentFields)

game_logic_collision_CAABoxShape2D = Object({
    **game_logic_collision_CShapeFields,
    "v2Min": common_types.CVector2D,
    "v2Max": common_types.CVector2D,
    "bOutwardsNormal": construct.Flag,
})

game_logic_collision_CCapsuleShape2D = Object({
    **game_logic_collision_CShapeFields,
    "fRadius": common_types.Float,
    "fHalfHeight": common_types.Float,
    "bOutwardsNormal": construct.Flag,
})

game_logic_collision_CCircleShape2D = Object({
    **game_logic_collision_CShapeFields,
    "fRadius": common_types.Float,
    "bOutwardsNormal": construct.Flag,
})

game_logic_collision_COBoxShape2D = Object({
    **game_logic_collision_CShapeFields,
    "v2Extent": common_types.CVector2D,
    "fDegrees": common_types.Float,
    "bOutwardsNormal": construct.Flag,
})

base_spatial_SSegmentData = Object({
    "vPos": common_types.CVector3D,
})

base_spatial_CPolygon2D = Object({
    "bClosed": construct.Flag,
    "oSegmentData": common_types.make_vector(base_spatial_SSegmentData),
    "bOutwardsNormal": construct.Flag,
})

base_spatial_CPolygonCollection2D = Object({
    "vPolys": common_types.make_vector(base_spatial_CPolygon2D),
})

game_logic_collision_CPolygonCollectionShape = Object({
    **game_logic_collision_CShapeFields,
    "oPolyCollection": base_spatial_CPolygonCollection2D,
})

CAllowCoolShinesparkLogicAction = Object({
    **CTriggerLogicActionFields,
    "lstAllowedDirections": common_types.make_vector(common_types.UInt),
    "lstAllowedSituations": common_types.make_vector(common_types.UInt),
    "sCoolShinesparkId": common_types.StrId,
    "bAllow": construct.Flag,
    "bForce": construct.Flag,
})

CCameraToRailLogicAction = Object({
    **CTriggerLogicActionFields,
    "bCameraToRail": construct.Flag,
})

CChangeSetupLogicAction = Object({
    **CTriggerLogicActionFields,
    "sSetupID": common_types.StrId,
    "bPersistent": construct.Flag,
    "bForceChange": construct.Flag,
    "bPush": construct.Flag,
})

DoorStateInfo = Object({
    "pDoor": common_types.StrId,
    "eDoorState": common_types.UInt,
})

CChangeStateDoorsLogicAction = Object({
    **CTriggerLogicActionFields,
    "vDoorStateInfo": common_types.make_vector(DoorStateInfo),
    "bEnabled": construct.Flag,
})

CCheckCoolShinesparkSuccessfullyCompletedLogicAction = Object(CTriggerLogicActionFields)

CMarkMinimapLogicAction = Object(CMarkMinimapLogicActionFields := {
    **CTriggerLogicActionFields,
    "wpVisibleLogicShape": common_types.StrId,
    "wpVisitedLogicShape": common_types.StrId,
})

CCoolShinesparkMarkMinimapLogicAction = Object(CMarkMinimapLogicActionFields)

CEmmyStateOverrideLogicAction = Object({
    **CTriggerLogicActionFields,
    "eMode": common_types.UInt,
})

CForbiddenEdgesLogicAction = Object({
    **CTriggerLogicActionFields,
    "eNavMeshGroup": common_types.UInt,
    "wpSpawnPoint": common_types.StrId,
    "wpLogicShape": common_types.StrId,
    "eState": common_types.UInt,
})

CForceMovementLogicAction = Object({
    **CTriggerLogicActionFields,
    "bMovePlayer": construct.Flag,
    "v2Direction": common_types.CVector2D,
})

CFreeAimTutoLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpItemToDestroy": common_types.StrId,
})

CHoldPlayerDirectionOnSubAreaChangeLogicAction = Object({
    **CTriggerLogicActionFields,
    "bForce": construct.Flag,
})

CIgnoreFloorSlideUpperBodySubmergedLogicAction = Object({
    **CTriggerLogicActionFields,
    "bActive": construct.Flag,
    "sId": common_types.StrId,
})

CItemDestructionLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpItemToDestroy": common_types.StrId,
    "wpObserver": common_types.StrId,
})

CLockRoomLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpAccessPoint": common_types.StrId,
    "sDoorsLockedLiteralID": common_types.StrId,
    "bInstantLock": construct.Flag,
})

CLuaCallsLogicAction = Object({
    **CTriggerLogicActionFields,
    "sCallbackEntityName": common_types.StrId,
    "sCallback": common_types.StrId,
    "bCallbackEntity": construct.Flag,
    "bCallbackPersistent": construct.Flag,
})

CPerceptionModifierLogicAction = Object({
    **CTriggerLogicActionFields,
    "eMode": common_types.UInt,
    "wpPerceivedPosition": common_types.StrId,
    "eGroup": common_types.UInt,
})

CSPBTutoLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpCentralUnitDoor": common_types.StrId,
    "wpCentralUnit": common_types.StrId,
    "oSPRTuto.m_vAfterTutoLogicActions": common_types.make_vector(Pointer_CTriggerLogicAction.create_construct()),
})

CSPRTutoLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpCentralUnitDoor": common_types.StrId,
    "wpCentralUnit": common_types.StrId,
    "vAfterTutoLogicActions": common_types.make_vector(Pointer_CTriggerLogicAction.create_construct()),
})

CSamusOverrideDistanceToBorderLogicAction = Object({
    **CTriggerLogicActionFields,
    "sId": common_types.StrId,
    "fLeftForwardDistance": common_types.Float,
    "fLeftBackwardDistance": common_types.Float,
    "fRightForwardDistance": common_types.Float,
    "fRightBackwardDistance": common_types.Float,
})

CSaveGameFromEmmyDoorLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpEmmyDoorActor": common_types.StrId,
    "bForce": construct.Flag,
    "bRestoreOriginalValue": construct.Flag,
})

CSaveGameLogicAction = Object({
    **CTriggerLogicActionFields,
    "eDestination": common_types.UInt,
    "sCheckpointKey": common_types.StrId,
    "wpStartPoint": common_types.StrId,
    "bForce": construct.Flag,
})

CSaveGameToSnapshotLogicAction = Object({
    **CTriggerLogicActionFields,
    "sSnapshotId": common_types.StrId,
})

CSaveSnapshotToCheckpointLogicAction = Object({
    **CTriggerLogicActionFields,
    "sSnapshotId": common_types.StrId,
    "sCheckpointKey": common_types.StrId,
    "wpStartPoint": common_types.StrId,
    "bForce": construct.Flag,
})

CSetActorEnabledLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpActor": common_types.StrId,
    "bEnabled": construct.Flag,
})

CShowPopUpCompositionLogicAction = Object({
    **CTriggerLogicActionFields,
    "vtexts": common_types.make_vector(common_types.StrId),
})

CStartCentralUnitCombatLogicAction = Object({
    **CTriggerLogicActionFields,
    "wpCentralUnit": common_types.StrId,
})

CSubareaTransitionTypeLogicAction = Object({
    **CTriggerLogicActionFields,
    "eTransitionType": common_types.UInt,
})

CTutoEnterLogicAction = Object({
    **CTriggerLogicActionFields,
    "sLiteralID": common_types.StrId,
    "bShowMessage": construct.Flag,
    "bWaitForInput": construct.Flag,
    "wpObserver": common_types.StrId,
    "sLuaCallbackOnMessageClosed": common_types.StrId,
    "sMissionLogTutoId": common_types.StrId,
})

CTutoExitLogicAction = Object({
    **CTriggerLogicActionFields,
    "sMissionLogTutoId": common_types.StrId,
    "wpTriggerToDisable": common_types.StrId,
})

CXParasiteGoSpawnBehavior = Object({
    **CXParasiteBehaviorFields,
    "tSpawnPoints": common_types.make_vector(common_types.StrId),
})

CXParasiteGoTransformBehavior = Object({
    **CXParasiteBehaviorFields,
    "wpFromSpawnPoint": common_types.StrId,
    "tToSpawnPoints": common_types.make_vector(common_types.StrId),
})

CXParasiteStayOnPlaceBehavior = Object({
    **CXParasiteBehaviorFields,
    "wpStayPosLandmark": common_types.StrId,
})

CXParasiteWanderThenFleeBehavior = Object(CXParasiteBehaviorFields)

base_global_CRntFile = construct.Prefixed(construct.Int32ul, construct.GreedyBytes)

Pointer_CActor.add_option("CActor", CActor)
Pointer_CActor.add_option("CEntity", CEntity)

Pointer_CActorComponent.add_option("CActorComponent", CActorComponent)
Pointer_CActorComponent.add_option("CAIAttackComponent", CAIAttackComponent)
Pointer_CActorComponent.add_option("CAIComponent", CAIComponent)
Pointer_CActorComponent.add_option("CAIGrapplePointComponent", CAIGrapplePointComponent)
Pointer_CActorComponent.add_option("CAINavigationComponent", CAINavigationComponent)
Pointer_CActorComponent.add_option("CAISmartObjectComponent", CAISmartObjectComponent)
Pointer_CActorComponent.add_option("CAbilityComponent", CAbilityComponent)
Pointer_CActorComponent.add_option("CAccessPointCommanderComponent", CAccessPointCommanderComponent)
Pointer_CActorComponent.add_option("CAccessPointComponent", CAccessPointComponent)
Pointer_CActorComponent.add_option("CActionSwitcherComponent", CActionSwitcherComponent)
Pointer_CActorComponent.add_option("CActionSwitcherOnPullGrapplePointComponent", CActionSwitcherOnPullGrapplePointComponent)
Pointer_CActorComponent.add_option("CActivatableByProjectileComponent", CActivatableByProjectileComponent)
Pointer_CActorComponent.add_option("CActivatableComponent", CActivatableComponent)
Pointer_CActorComponent.add_option("CAimCameraEnabledVisibleOnlyComponent", CAimCameraEnabledVisibleOnlyComponent)
Pointer_CActorComponent.add_option("CAimComponent", CAimComponent)
Pointer_CActorComponent.add_option("CAlternativeActionPlayerComponent", CAlternativeActionPlayerComponent)
Pointer_CActorComponent.add_option("CAmmoRechargeComponent", CAmmoRechargeComponent)
Pointer_CActorComponent.add_option("CAnimationComponent", CAnimationComponent)
Pointer_CActorComponent.add_option("CAnimationNavMeshItemComponent", CAnimationNavMeshItemComponent)
Pointer_CActorComponent.add_option("CArachnusAIComponent", CArachnusAIComponent)
Pointer_CActorComponent.add_option("CAreaFXComponent", CAreaFXComponent)
Pointer_CActorComponent.add_option("CAreaMusicComponent", CAreaMusicComponent)
Pointer_CActorComponent.add_option("CAreaSoundComponent", CAreaSoundComponent)
Pointer_CActorComponent.add_option("CAttackComponent", CAttackComponent)
Pointer_CActorComponent.add_option("CAudioComponent", CAudioComponent)
Pointer_CActorComponent.add_option("CAutclastAIComponent", CAutclastAIComponent)
Pointer_CActorComponent.add_option("CAutectorAIComponent", CAutectorAIComponent)
Pointer_CActorComponent.add_option("CAutectorLifeComponent", CAutectorLifeComponent)
Pointer_CActorComponent.add_option("CAutomperAIComponent", CAutomperAIComponent)
Pointer_CActorComponent.add_option("CAutoolAIComponent", CAutoolAIComponent)
Pointer_CActorComponent.add_option("CAutsharpAIComponent", CAutsharpAIComponent)
Pointer_CActorComponent.add_option("CAutsharpLifeComponent", CAutsharpLifeComponent)
Pointer_CActorComponent.add_option("CAutsharpSpawnPointComponent", CAutsharpSpawnPointComponent)
Pointer_CActorComponent.add_option("CAutsniperAIComponent", CAutsniperAIComponent)
Pointer_CActorComponent.add_option("CAutsniperSpawnPointComponent", CAutsniperSpawnPointComponent)
Pointer_CActorComponent.add_option("CBTObserverComponent", CBTObserverComponent)
Pointer_CActorComponent.add_option("CBaseBigFistAIComponent", CBaseBigFistAIComponent)
Pointer_CActorComponent.add_option("CBaseDamageTriggerComponent", CBaseDamageTriggerComponent)
Pointer_CActorComponent.add_option("CBaseGroundShockerAIComponent", CBaseGroundShockerAIComponent)
Pointer_CActorComponent.add_option("CBaseLightComponent", CBaseLightComponent)
Pointer_CActorComponent.add_option("CBaseTriggerComponent", CBaseTriggerComponent)
Pointer_CActorComponent.add_option("CBasicLifeComponent", CBasicLifeComponent)
Pointer_CActorComponent.add_option("CBatalloonAIComponent", CBatalloonAIComponent)
Pointer_CActorComponent.add_option("CBeamBoxComponent", CBeamBoxComponent)
Pointer_CActorComponent.add_option("CBeamDoorLifeComponent", CBeamDoorLifeComponent)
Pointer_CActorComponent.add_option("CBehaviorTreeAIComponent", CBehaviorTreeAIComponent)
Pointer_CActorComponent.add_option("CBigFistAIComponent", CBigFistAIComponent)
Pointer_CActorComponent.add_option("CBigkranXAIComponent", CBigkranXAIComponent)
Pointer_CActorComponent.add_option("CBillboardCollisionComponent", CBillboardCollisionComponent)
Pointer_CActorComponent.add_option("CBillboardComponent", CBillboardComponent)
Pointer_CActorComponent.add_option("CBillboardLifeComponent", CBillboardLifeComponent)
Pointer_CActorComponent.add_option("CBombMovement", CBombMovement)
Pointer_CActorComponent.add_option("CBoneToConstantComponent", CBoneToConstantComponent)
Pointer_CActorComponent.add_option("CBossAIComponent", CBossAIComponent)
Pointer_CActorComponent.add_option("CBossLifeComponent", CBossLifeComponent)
Pointer_CActorComponent.add_option("CBossSpawnGroupComponent", CBossSpawnGroupComponent)
Pointer_CActorComponent.add_option("CBreakableHintComponent", CBreakableHintComponent)
Pointer_CActorComponent.add_option("CBreakableScenarioComponent", CBreakableScenarioComponent)
Pointer_CActorComponent.add_option("CBreakableTileGroupComponent", CBreakableTileGroupComponent)
Pointer_CActorComponent.add_option("CBreakableTileGroupSonarTargetComponent", CBreakableTileGroupSonarTargetComponent)
Pointer_CActorComponent.add_option("CBreakableVignetteComponent", CBreakableVignetteComponent)
Pointer_CActorComponent.add_option("CCameraComponent", CCameraComponent)
Pointer_CActorComponent.add_option("CCameraRailComponent", CCameraRailComponent)
Pointer_CActorComponent.add_option("CCapsuleUsableComponent", CCapsuleUsableComponent)
Pointer_CActorComponent.add_option("CCaterzillaAIComponent", CCaterzillaAIComponent)
Pointer_CActorComponent.add_option("CCaterzillaSpawnPointComponent", CCaterzillaSpawnPointComponent)
Pointer_CActorComponent.add_option("CCaveCentralUnitComponent", CCaveCentralUnitComponent)
Pointer_CActorComponent.add_option("CCentralUnitAIComponent", CCentralUnitAIComponent)
Pointer_CActorComponent.add_option("CCentralUnitCannonAIComponent", CCentralUnitCannonAIComponent)
Pointer_CActorComponent.add_option("CCentralUnitCannonBeamMovementComponent", CCentralUnitCannonBeamMovementComponent)
Pointer_CActorComponent.add_option("CCentralUnitComponent", CCentralUnitComponent)
Pointer_CActorComponent.add_option("CChainReactionActionSwitcherComponent", CChainReactionActionSwitcherComponent)
Pointer_CActorComponent.add_option("CChangeStageNavMeshItemComponent", CChangeStageNavMeshItemComponent)
Pointer_CActorComponent.add_option("CCharacterLifeComponent", CCharacterLifeComponent)
Pointer_CActorComponent.add_option("CCharacterMovement", CCharacterMovement)
Pointer_CActorComponent.add_option("CChozoCommanderAIComponent", CChozoCommanderAIComponent)
Pointer_CActorComponent.add_option("CChozoCommanderEnergyShardsFragmentMovementComponent", CChozoCommanderEnergyShardsFragmentMovementComponent)
Pointer_CActorComponent.add_option("CChozoCommanderEnergyShardsSphereMovementComponent", CChozoCommanderEnergyShardsSphereMovementComponent)
Pointer_CActorComponent.add_option("CChozoCommanderSentenceSphereLifeComponent", CChozoCommanderSentenceSphereLifeComponent)
Pointer_CActorComponent.add_option("CChozoCommanderSentenceSphereMovementComponent", CChozoCommanderSentenceSphereMovementComponent)
Pointer_CActorComponent.add_option("CChozoCommanderXLifeComponent", CChozoCommanderXLifeComponent)
Pointer_CActorComponent.add_option("CChozoRobotSoldierAIComponent", CChozoRobotSoldierAIComponent)
Pointer_CActorComponent.add_option("CChozoRobotSoldierBeamMovementComponent", CChozoRobotSoldierBeamMovementComponent)
Pointer_CActorComponent.add_option("CChozoWarriorAIComponent", CChozoWarriorAIComponent)
Pointer_CActorComponent.add_option("CChozoWarriorEliteAIComponent", CChozoWarriorEliteAIComponent)
Pointer_CActorComponent.add_option("CChozoWarriorXAIComponent", CChozoWarriorXAIComponent)
Pointer_CActorComponent.add_option("CChozoWarriorXEliteAIComponent", CChozoWarriorXEliteAIComponent)
Pointer_CActorComponent.add_option("CChozoWarriorXSpitMovementComponent", CChozoWarriorXSpitMovementComponent)
Pointer_CActorComponent.add_option("CChozoZombieXAIComponent", CChozoZombieXAIComponent)
Pointer_CActorComponent.add_option("CChozoZombieXSpawnPointComponent", CChozoZombieXSpawnPointComponent)
Pointer_CActorComponent.add_option("CChozombieFXComponent", CChozombieFXComponent)
Pointer_CActorComponent.add_option("CColliderTriggerComponent", CColliderTriggerComponent)
Pointer_CActorComponent.add_option("CCollisionComponent", CCollisionComponent)
Pointer_CActorComponent.add_option("CCollisionMaterialCacheComponent", CCollisionMaterialCacheComponent)
Pointer_CActorComponent.add_option("CComponent", CComponent)
Pointer_CActorComponent.add_option("CConstantMovement", CConstantMovement)
Pointer_CActorComponent.add_option("CCooldownXBossAIComponent", CCooldownXBossAIComponent)
Pointer_CActorComponent.add_option("CCooldownXBossFireBallMovementComponent", CCooldownXBossFireBallMovementComponent)
Pointer_CActorComponent.add_option("CCooldownXBossWeakPointLifeComponent", CCooldownXBossWeakPointLifeComponent)
Pointer_CActorComponent.add_option("CCoreXAIComponent", CCoreXAIComponent)
Pointer_CActorComponent.add_option("CCubeMapComponent", CCubeMapComponent)
Pointer_CActorComponent.add_option("CCutsceneComponent", CCutsceneComponent)
Pointer_CActorComponent.add_option("CCutsceneTriggerComponent", CCutsceneTriggerComponent)
Pointer_CActorComponent.add_option("CDaivoAIComponent", CDaivoAIComponent)
Pointer_CActorComponent.add_option("CDaivoSwarmControllerComponent", CDaivoSwarmControllerComponent)
Pointer_CActorComponent.add_option("CDamageComponent", CDamageComponent)
Pointer_CActorComponent.add_option("CDamageTriggerComponent", CDamageTriggerComponent)
Pointer_CActorComponent.add_option("CDemolitionBlockActivatableActorLifeComponent", CDemolitionBlockActivatableActorLifeComponent)
Pointer_CActorComponent.add_option("CDemolitionBlockComponent", CDemolitionBlockComponent)
Pointer_CActorComponent.add_option("CDemolitionBlockLifeComponent", CDemolitionBlockLifeComponent)
Pointer_CActorComponent.add_option("CDemolitionBlockSonarTargetComponent", CDemolitionBlockSonarTargetComponent)
Pointer_CActorComponent.add_option("CDirLightComponent", CDirLightComponent)
Pointer_CActorComponent.add_option("CDizzeanSwarmControllerComponent", CDizzeanSwarmControllerComponent)
Pointer_CActorComponent.add_option("CDoorCentralUnitLifeComponent", CDoorCentralUnitLifeComponent)
Pointer_CActorComponent.add_option("CDoorEmmyFXComponent", CDoorEmmyFXComponent)
Pointer_CActorComponent.add_option("CDoorGrapplePointComponent", CDoorGrapplePointComponent)
Pointer_CActorComponent.add_option("CDoorLifeComponent", CDoorLifeComponent)
Pointer_CActorComponent.add_option("CDoorShieldLifeComponent", CDoorShieldLifeComponent)
Pointer_CActorComponent.add_option("CDredhedAIComponent", CDredhedAIComponent)
Pointer_CActorComponent.add_option("CDredhedAttackComponent", CDredhedAttackComponent)
Pointer_CActorComponent.add_option("CDropComponent", CDropComponent)
Pointer_CActorComponent.add_option("CDroppableComponent", CDroppableComponent)
Pointer_CActorComponent.add_option("CDroppableLifeComponent", CDroppableLifeComponent)
Pointer_CActorComponent.add_option("CDroppableMissileComponent", CDroppableMissileComponent)
Pointer_CActorComponent.add_option("CDroppablePowerBombComponent", CDroppablePowerBombComponent)
Pointer_CActorComponent.add_option("CDroppableSpecialEnergyComponent", CDroppableSpecialEnergyComponent)
Pointer_CActorComponent.add_option("CDropterAIComponent", CDropterAIComponent)
Pointer_CActorComponent.add_option("CDummyAIComponent", CDummyAIComponent)
Pointer_CActorComponent.add_option("CDummyMovement", CDummyMovement)
Pointer_CActorComponent.add_option("CDummyPullableGrapplePointComponent", CDummyPullableGrapplePointComponent)
Pointer_CActorComponent.add_option("CElectricGeneratorComponent", CElectricGeneratorComponent)
Pointer_CActorComponent.add_option("CElectricReactionComponent", CElectricReactionComponent)
Pointer_CActorComponent.add_option("CElectrifyingAreaComponent", CElectrifyingAreaComponent)
Pointer_CActorComponent.add_option("CElevatorCommanderUsableComponent", CElevatorCommanderUsableComponent)
Pointer_CActorComponent.add_option("CElevatorUsableComponent", CElevatorUsableComponent)
Pointer_CActorComponent.add_option("CEmergencyLightElectricReactionComponent", CEmergencyLightElectricReactionComponent)
Pointer_CActorComponent.add_option("CEmmyAIComponent", CEmmyAIComponent)
Pointer_CActorComponent.add_option("CEmmyAttackComponent", CEmmyAttackComponent)
Pointer_CActorComponent.add_option("CEmmyCaveAIComponent", CEmmyCaveAIComponent)
Pointer_CActorComponent.add_option("CEmmyForestAIComponent", CEmmyForestAIComponent)
Pointer_CActorComponent.add_option("CEmmyLabAIComponent", CEmmyLabAIComponent)
Pointer_CActorComponent.add_option("CEmmyMagmaAIComponent", CEmmyMagmaAIComponent)
Pointer_CActorComponent.add_option("CEmmyMovement", CEmmyMovement)
Pointer_CActorComponent.add_option("CEmmyProtoAIComponent", CEmmyProtoAIComponent)
Pointer_CActorComponent.add_option("CEmmySancAIComponent", CEmmySancAIComponent)
Pointer_CActorComponent.add_option("CEmmyShipyardAIComponent", CEmmyShipyardAIComponent)
Pointer_CActorComponent.add_option("CEmmySpawnPointComponent", CEmmySpawnPointComponent)
Pointer_CActorComponent.add_option("CEmmyValveComponent", CEmmyValveComponent)
Pointer_CActorComponent.add_option("CEmmyWakeUpComponent", CEmmyWakeUpComponent)
Pointer_CActorComponent.add_option("CEmmyWaveMovementComponent", CEmmyWaveMovementComponent)
Pointer_CActorComponent.add_option("CEnemyLifeComponent", CEnemyLifeComponent)
Pointer_CActorComponent.add_option("CEnemyMovement", CEnemyMovement)
Pointer_CActorComponent.add_option("CEnhanceWeakSpotComponent", CEnhanceWeakSpotComponent)
Pointer_CActorComponent.add_option("CEscapeSequenceExplosionComponent", CEscapeSequenceExplosionComponent)
Pointer_CActorComponent.add_option("CEvacuationCountDown", CEvacuationCountDown)
Pointer_CActorComponent.add_option("CEventPropComponent", CEventPropComponent)
Pointer_CActorComponent.add_option("CEventScenarioComponent", CEventScenarioComponent)
Pointer_CActorComponent.add_option("CFXComponent", CFXComponent)
Pointer_CActorComponent.add_option("CFactionComponent", CFactionComponent)
Pointer_CActorComponent.add_option("CFakePhysicsMovement", CFakePhysicsMovement)
Pointer_CActorComponent.add_option("CFanComponent", CFanComponent)
Pointer_CActorComponent.add_option("CFanCoolDownComponent", CFanCoolDownComponent)
Pointer_CActorComponent.add_option("CFingSwarmControllerComponent", CFingSwarmControllerComponent)
Pointer_CActorComponent.add_option("CFireComponent", CFireComponent)
Pointer_CActorComponent.add_option("CFloatingPropActingComponent", CFloatingPropActingComponent)
Pointer_CActorComponent.add_option("CFlockingSwarmControllerComponent", CFlockingSwarmControllerComponent)
Pointer_CActorComponent.add_option("CFloorShockWaveComponent", CFloorShockWaveComponent)
Pointer_CActorComponent.add_option("CFootstepPlatformComponent", CFootstepPlatformComponent)
Pointer_CActorComponent.add_option("CForcedMovementAreaComponent", CForcedMovementAreaComponent)
Pointer_CActorComponent.add_option("CFreezeRoomComponent", CFreezeRoomComponent)
Pointer_CActorComponent.add_option("CFrozenAsFrostbiteComponent", CFrozenAsFrostbiteComponent)
Pointer_CActorComponent.add_option("CFrozenAsPlatformComponent", CFrozenAsPlatformComponent)
Pointer_CActorComponent.add_option("CFrozenComponent", CFrozenComponent)
Pointer_CActorComponent.add_option("CFrozenPlatformComponent", CFrozenPlatformComponent)
Pointer_CActorComponent.add_option("CFulmiteBellyMineAIComponent", CFulmiteBellyMineAIComponent)
Pointer_CActorComponent.add_option("CFulmiteBellyMineAttackComponent", CFulmiteBellyMineAttackComponent)
Pointer_CActorComponent.add_option("CFulmiteBellyMineMovementComponent", CFulmiteBellyMineMovementComponent)
Pointer_CActorComponent.add_option("CFusibleBoxComponent", CFusibleBoxComponent)
Pointer_CActorComponent.add_option("CGobblerAIComponent", CGobblerAIComponent)
Pointer_CActorComponent.add_option("CGobblerSpawnPointComponent", CGobblerSpawnPointComponent)
Pointer_CActorComponent.add_option("CGoliathAIComponent", CGoliathAIComponent)
Pointer_CActorComponent.add_option("CGoliathXAIComponent", CGoliathXAIComponent)
Pointer_CActorComponent.add_option("CGoliathXBurstProjectionBombMovement", CGoliathXBurstProjectionBombMovement)
Pointer_CActorComponent.add_option("CGooplotAIComponent", CGooplotAIComponent)
Pointer_CActorComponent.add_option("CGooshockerAIComponent", CGooshockerAIComponent)
Pointer_CActorComponent.add_option("CGrabComponent", CGrabComponent)
Pointer_CActorComponent.add_option("CGrappleBeamComponent", CGrappleBeamComponent)
Pointer_CActorComponent.add_option("CGrapplePointComponent", CGrapplePointComponent)
Pointer_CActorComponent.add_option("CGroundShockerAIComponent", CGroundShockerAIComponent)
Pointer_CActorComponent.add_option("CGunComponent", CGunComponent)
Pointer_CActorComponent.add_option("CHangableGrappleMagnetSlidingBlockComponent", CHangableGrappleMagnetSlidingBlockComponent)
Pointer_CActorComponent.add_option("CHangableGrapplePointComponent", CHangableGrapplePointComponent)
Pointer_CActorComponent.add_option("CHangableGrappleSurfaceComponent", CHangableGrappleSurfaceComponent)
Pointer_CActorComponent.add_option("CHeatRoomComponent", CHeatRoomComponent)
Pointer_CActorComponent.add_option("CHeatableShieldComponent", CHeatableShieldComponent)
Pointer_CActorComponent.add_option("CHeatableShieldEnhanceWeakSpotComponent", CHeatableShieldEnhanceWeakSpotComponent)
Pointer_CActorComponent.add_option("CHecathonAIComponent", CHecathonAIComponent)
Pointer_CActorComponent.add_option("CHecathonLifeComponent", CHecathonLifeComponent)
Pointer_CActorComponent.add_option("CHecathonPlanktonFXComponent", CHecathonPlanktonFXComponent)
Pointer_CActorComponent.add_option("CHomingMovement", CHomingMovement)
Pointer_CActorComponent.add_option("CHydrogigaAIComponent", CHydrogigaAIComponent)
Pointer_CActorComponent.add_option("CHydrogigaZiplineComponent", CHydrogigaZiplineComponent)
Pointer_CActorComponent.add_option("CHydrogigaZiplineRailComponent", CHydrogigaZiplineRailComponent)
Pointer_CActorComponent.add_option("CHyperBeamBlockLifeComponent", CHyperBeamBlockLifeComponent)
Pointer_CActorComponent.add_option("CIceMissileMovement", CIceMissileMovement)
Pointer_CActorComponent.add_option("CInfesterAIComponent", CInfesterAIComponent)
Pointer_CActorComponent.add_option("CInfesterBallAIComponent", CInfesterBallAIComponent)
Pointer_CActorComponent.add_option("CInfesterBallAttackComponent", CInfesterBallAttackComponent)
Pointer_CActorComponent.add_option("CInfesterBallLifeComponent", CInfesterBallLifeComponent)
Pointer_CActorComponent.add_option("CInfesterBallMovementComponent", CInfesterBallMovementComponent)
Pointer_CActorComponent.add_option("CInputComponent", CInputComponent)
Pointer_CActorComponent.add_option("CInterpolationComponent", CInterpolationComponent)
Pointer_CActorComponent.add_option("CInventoryComponent", CInventoryComponent)
Pointer_CActorComponent.add_option("CItemLifeComponent", CItemLifeComponent)
Pointer_CActorComponent.add_option("CKraidAIComponent", CKraidAIComponent)
Pointer_CActorComponent.add_option("CKraidAcidBlobsMovementComponent", CKraidAcidBlobsMovementComponent)
Pointer_CActorComponent.add_option("CKraidBouncingCreaturesMovementComponent", CKraidBouncingCreaturesMovementComponent)
Pointer_CActorComponent.add_option("CKraidNailMovementComponent", CKraidNailMovementComponent)
Pointer_CActorComponent.add_option("CKraidShockerSplashMovementComponent", CKraidShockerSplashMovementComponent)
Pointer_CActorComponent.add_option("CKraidSpikeMovablePlatformComponent", CKraidSpikeMovablePlatformComponent)
Pointer_CActorComponent.add_option("CLandmarkComponent", CLandmarkComponent)
Pointer_CActorComponent.add_option("CLavaPoolComponent", CLavaPoolComponent)
Pointer_CActorComponent.add_option("CLavaPumpComponent", CLavaPumpComponent)
Pointer_CActorComponent.add_option("CLavapumpThermalReactionComponent", CLavapumpThermalReactionComponent)
Pointer_CActorComponent.add_option("CLifeComponent", CLifeComponent)
Pointer_CActorComponent.add_option("CLifeRechargeComponent", CLifeRechargeComponent)
Pointer_CActorComponent.add_option("CLightingComponent", CLightingComponent)
Pointer_CActorComponent.add_option("CLineBombMovement", CLineBombMovement)
Pointer_CActorComponent.add_option("CLiquidPoolBaseComponent", CLiquidPoolBaseComponent)
Pointer_CActorComponent.add_option("CLiquidSimulationComponent", CLiquidSimulationComponent)
Pointer_CActorComponent.add_option("CLockOnMissileMovement", CLockOnMissileMovement)
Pointer_CActorComponent.add_option("CLogicActionTriggerComponent", CLogicActionTriggerComponent)
Pointer_CActorComponent.add_option("CLogicCameraComponent", CLogicCameraComponent)
Pointer_CActorComponent.add_option("CLogicLookAtPlayerComponent", CLogicLookAtPlayerComponent)
Pointer_CActorComponent.add_option("CLogicPathComponent", CLogicPathComponent)
Pointer_CActorComponent.add_option("CLogicPathNavMeshItemComponent", CLogicPathNavMeshItemComponent)
Pointer_CActorComponent.add_option("CLogicShapeComponent", CLogicShapeComponent)
Pointer_CActorComponent.add_option("CMagmaCentralUnitComponent", CMagmaCentralUnitComponent)
Pointer_CActorComponent.add_option("CMagmaKraidPistonPlatformComponent", CMagmaKraidPistonPlatformComponent)
Pointer_CActorComponent.add_option("CMagmaKraidScenarioControllerComponent", CMagmaKraidScenarioControllerComponent)
Pointer_CActorComponent.add_option("CMagmaKraidSpikeComponent", CMagmaKraidSpikeComponent)
Pointer_CActorComponent.add_option("CMagnetMovablePlatformComponent", CMagnetMovablePlatformComponent)
Pointer_CActorComponent.add_option("CMagnetSlidingBlockComponent", CMagnetSlidingBlockComponent)
Pointer_CActorComponent.add_option("CMagnetSlidingBlockCounterWeightMovablePlatformComponent", CMagnetSlidingBlockCounterWeightMovablePlatformComponent)
Pointer_CActorComponent.add_option("CMagnetSlidingBlockRailComponent", CMagnetSlidingBlockRailComponent)
Pointer_CActorComponent.add_option("CMagnetSlidingBlockWithCollisionsComponent", CMagnetSlidingBlockWithCollisionsComponent)
Pointer_CActorComponent.add_option("CMagnetSurfaceComponent", CMagnetSurfaceComponent)
Pointer_CActorComponent.add_option("CMagnetSurfaceHuskComponent", CMagnetSurfaceHuskComponent)
Pointer_CActorComponent.add_option("CMapAcquisitionComponent", CMapAcquisitionComponent)
Pointer_CActorComponent.add_option("CMassiveCaterzillaSpawnGroupComponent", CMassiveCaterzillaSpawnGroupComponent)
Pointer_CActorComponent.add_option("CMaterialFXComponent", CMaterialFXComponent)
Pointer_CActorComponent.add_option("CMeleeComponent", CMeleeComponent)
Pointer_CActorComponent.add_option("CMenuAnimationChangeComponent", CMenuAnimationChangeComponent)
Pointer_CActorComponent.add_option("CMissileMovement", CMissileMovement)
Pointer_CActorComponent.add_option("CModelInstanceComponent", CModelInstanceComponent)
Pointer_CActorComponent.add_option("CModelUpdaterComponent", CModelUpdaterComponent)
Pointer_CActorComponent.add_option("CMorphBallLauncherComponent", CMorphBallLauncherComponent)
Pointer_CActorComponent.add_option("CMorphBallLauncherExitComponent", CMorphBallLauncherExitComponent)
Pointer_CActorComponent.add_option("CMorphBallMovement", CMorphBallMovement)
Pointer_CActorComponent.add_option("CMovableGrapplePointComponent", CMovableGrapplePointComponent)
Pointer_CActorComponent.add_option("CMovablePlatformComponent", CMovablePlatformComponent)
Pointer_CActorComponent.add_option("CMovementComponent", CMovementComponent)
Pointer_CActorComponent.add_option("CMultiLockOnBlockComponent", CMultiLockOnBlockComponent)
Pointer_CActorComponent.add_option("CMultiLockOnPointComponent", CMultiLockOnPointComponent)
Pointer_CActorComponent.add_option("CMultiModelUpdaterComponent", CMultiModelUpdaterComponent)
Pointer_CActorComponent.add_option("CMushroomPlatformComponent", CMushroomPlatformComponent)
Pointer_CActorComponent.add_option("CNailongAIComponent", CNailongAIComponent)
Pointer_CActorComponent.add_option("CNailongThornMovementComponent", CNailongThornMovementComponent)
Pointer_CActorComponent.add_option("CNailuggerAcidBallMovementComponent", CNailuggerAcidBallMovementComponent)
Pointer_CActorComponent.add_option("CNavMeshItemComponent", CNavMeshItemComponent)
Pointer_CActorComponent.add_option("CNoFreezeRoomComponent", CNoFreezeRoomComponent)
Pointer_CActorComponent.add_option("CObsydomithonAIComponent", CObsydomithonAIComponent)
Pointer_CActorComponent.add_option("COmniLightComponent", COmniLightComponent)
Pointer_CActorComponent.add_option("CPerceptionComponent", CPerceptionComponent)
Pointer_CActorComponent.add_option("CPersistenceComponent", CPersistenceComponent)
Pointer_CActorComponent.add_option("CPickableComponent", CPickableComponent)
Pointer_CActorComponent.add_option("CPickableItemComponent", CPickableItemComponent)
Pointer_CActorComponent.add_option("CPickableSpringBallComponent", CPickableSpringBallComponent)
Pointer_CActorComponent.add_option("CPickableSuitComponent", CPickableSuitComponent)
Pointer_CActorComponent.add_option("CPlatformTrapGrapplePointComponent", CPlatformTrapGrapplePointComponent)
Pointer_CActorComponent.add_option("CPlayerLifeComponent", CPlayerLifeComponent)
Pointer_CActorComponent.add_option("CPlayerMovement", CPlayerMovement)
Pointer_CActorComponent.add_option("CPoisonFlyAIComponent", CPoisonFlyAIComponent)
Pointer_CActorComponent.add_option("CPositionalSoundComponent", CPositionalSoundComponent)
Pointer_CActorComponent.add_option("CPowerBombBlockLifeComponent", CPowerBombBlockLifeComponent)
Pointer_CActorComponent.add_option("CPowerBombMovement", CPowerBombMovement)
Pointer_CActorComponent.add_option("CPowerGeneratorComponent", CPowerGeneratorComponent)
Pointer_CActorComponent.add_option("CPowerUpLifeComponent", CPowerUpLifeComponent)
Pointer_CActorComponent.add_option("CProfessorDoorComponent", CProfessorDoorComponent)
Pointer_CActorComponent.add_option("CProjectileMovement", CProjectileMovement)
Pointer_CActorComponent.add_option("CProtoCentralUnitComponent", CProtoCentralUnitComponent)
Pointer_CActorComponent.add_option("CProtoEmmyChaseMusicTriggerComponent", CProtoEmmyChaseMusicTriggerComponent)
Pointer_CActorComponent.add_option("CPullOffGrapplePointComponent", CPullOffGrapplePointComponent)
Pointer_CActorComponent.add_option("CPullableGrapplePointComponent", CPullableGrapplePointComponent)
Pointer_CActorComponent.add_option("CQuarentineDoorComponent", CQuarentineDoorComponent)
Pointer_CActorComponent.add_option("CQuetzoaAIComponent", CQuetzoaAIComponent)
Pointer_CActorComponent.add_option("CQuetzoaEnergyWaveMovementComponent", CQuetzoaEnergyWaveMovementComponent)
Pointer_CActorComponent.add_option("CQuetzoaMultiTargetProjectileMovementComponent", CQuetzoaMultiTargetProjectileMovementComponent)
Pointer_CActorComponent.add_option("CQuetzoaXAIComponent", CQuetzoaXAIComponent)
Pointer_CActorComponent.add_option("CRedenkiSwarmControllerComponent", CRedenkiSwarmControllerComponent)
Pointer_CActorComponent.add_option("CReturnAreaSmartObjectComponent", CReturnAreaSmartObjectComponent)
Pointer_CActorComponent.add_option("CRinkaAIComponent", CRinkaAIComponent)
Pointer_CActorComponent.add_option("CRinkaUnitComponent", CRinkaUnitComponent)
Pointer_CActorComponent.add_option("CRobotAIComponent", CRobotAIComponent)
Pointer_CActorComponent.add_option("CRockDiverAIComponent", CRockDiverAIComponent)
Pointer_CActorComponent.add_option("CRockDiverSpawnPointComponent", CRockDiverSpawnPointComponent)
Pointer_CActorComponent.add_option("CRodomithonXAIComponent", CRodomithonXAIComponent)
Pointer_CActorComponent.add_option("CRodotukAIComponent", CRodotukAIComponent)
Pointer_CActorComponent.add_option("CRotationalPlatformComponent", CRotationalPlatformComponent)
Pointer_CActorComponent.add_option("CRumbleComponent", CRumbleComponent)
Pointer_CActorComponent.add_option("CSabotoruAIComponent", CSabotoruAIComponent)
Pointer_CActorComponent.add_option("CSabotoruLifeComponent", CSabotoruLifeComponent)
Pointer_CActorComponent.add_option("CSabotoruSpawnPointComponent", CSabotoruSpawnPointComponent)
Pointer_CActorComponent.add_option("CSamusAlternativeActionPlayerComponent", CSamusAlternativeActionPlayerComponent)
Pointer_CActorComponent.add_option("CSamusAnimationComponent", CSamusAnimationComponent)
Pointer_CActorComponent.add_option("CSamusGunComponent", CSamusGunComponent)
Pointer_CActorComponent.add_option("CSamusModelUpdaterComponent", CSamusModelUpdaterComponent)
Pointer_CActorComponent.add_option("CSamusMovement", CSamusMovement)
Pointer_CActorComponent.add_option("CSaveStationUsableComponent", CSaveStationUsableComponent)
Pointer_CActorComponent.add_option("CSceneComponent", CSceneComponent)
Pointer_CActorComponent.add_option("CSceneModelAnimationComponent", CSceneModelAnimationComponent)
Pointer_CActorComponent.add_option("CSclawkAIComponent", CSclawkAIComponent)
Pointer_CActorComponent.add_option("CSclawkLifeComponent", CSclawkLifeComponent)
Pointer_CActorComponent.add_option("CScorpiusAIComponent", CScorpiusAIComponent)
Pointer_CActorComponent.add_option("CScorpiusFXComponent", CScorpiusFXComponent)
Pointer_CActorComponent.add_option("CScorpiusPoisonousSpitMovementComponent", CScorpiusPoisonousSpitMovementComponent)
Pointer_CActorComponent.add_option("CScourgeAIComponent", CScourgeAIComponent)
Pointer_CActorComponent.add_option("CScourgeLifeComponent", CScourgeLifeComponent)
Pointer_CActorComponent.add_option("CScriptComponent", CScriptComponent)
Pointer_CActorComponent.add_option("CSegmentLightComponent", CSegmentLightComponent)
Pointer_CActorComponent.add_option("CSensorDoorComponent", CSensorDoorComponent)
Pointer_CActorComponent.add_option("CShakernautAIComponent", CShakernautAIComponent)
Pointer_CActorComponent.add_option("CShelmitAIComponent", CShelmitAIComponent)
Pointer_CActorComponent.add_option("CShineonAIComponent", CShineonAIComponent)
Pointer_CActorComponent.add_option("CShipRechargeComponent", CShipRechargeComponent)
Pointer_CActorComponent.add_option("CShockWaveComponent", CShockWaveComponent)
Pointer_CActorComponent.add_option("CShockWavePoolComponent", CShockWavePoolComponent)
Pointer_CActorComponent.add_option("CShootActivatorComponent", CShootActivatorComponent)
Pointer_CActorComponent.add_option("CShootActivatorHidrogigaComponent", CShootActivatorHidrogigaComponent)
Pointer_CActorComponent.add_option("CShotComponent", CShotComponent)
Pointer_CActorComponent.add_option("CSideEnemyMovement", CSideEnemyMovement)
Pointer_CActorComponent.add_option("CSlidleSpawnPointComponent", CSlidleSpawnPointComponent)
Pointer_CActorComponent.add_option("CSlowNailongSpawnPointComponent", CSlowNailongSpawnPointComponent)
Pointer_CActorComponent.add_option("CSluggerAIComponent", CSluggerAIComponent)
Pointer_CActorComponent.add_option("CSluggerAcidBallMovementComponent", CSluggerAcidBallMovementComponent)
Pointer_CActorComponent.add_option("CSmartObjectComponent", CSmartObjectComponent)
Pointer_CActorComponent.add_option("CSonarTargetComponent", CSonarTargetComponent)
Pointer_CActorComponent.add_option("CSoundListenerComponent", CSoundListenerComponent)
Pointer_CActorComponent.add_option("CSoundProofTriggerComponent", CSoundProofTriggerComponent)
Pointer_CActorComponent.add_option("CSoundTrigger", CSoundTrigger)
Pointer_CActorComponent.add_option("CSpawnGroupComponent", CSpawnGroupComponent)
Pointer_CActorComponent.add_option("CSpawnPointComponent", CSpawnPointComponent)
Pointer_CActorComponent.add_option("CSpbSprActivator", CSpbSprActivator)
Pointer_CActorComponent.add_option("CSpecialEnergyComponent", CSpecialEnergyComponent)
Pointer_CActorComponent.add_option("CSpitclawkAIComponent", CSpitclawkAIComponent)
Pointer_CActorComponent.add_option("CSpittailMagmaBallMovementComponent", CSpittailMagmaBallMovementComponent)
Pointer_CActorComponent.add_option("CSpotLightComponent", CSpotLightComponent)
Pointer_CActorComponent.add_option("CStandaloneFXComponent", CStandaloneFXComponent)
Pointer_CActorComponent.add_option("CStartPointComponent", CStartPointComponent)
Pointer_CActorComponent.add_option("CSteamJetComponent", CSteamJetComponent)
Pointer_CActorComponent.add_option("CSteeringMovement", CSteeringMovement)
Pointer_CActorComponent.add_option("CSunnapAIComponent", CSunnapAIComponent)
Pointer_CActorComponent.add_option("CSuperMissileMovement", CSuperMissileMovement)
Pointer_CActorComponent.add_option("CSwarmAttackComponent", CSwarmAttackComponent)
Pointer_CActorComponent.add_option("CSwarmControllerComponent", CSwarmControllerComponent)
Pointer_CActorComponent.add_option("CSwifterAIComponent", CSwifterAIComponent)
Pointer_CActorComponent.add_option("CSwifterSpawnGroupComponent", CSwifterSpawnGroupComponent)
Pointer_CActorComponent.add_option("CSwingableGrapplePointComponent", CSwingableGrapplePointComponent)
Pointer_CActorComponent.add_option("CTakumakuAIComponent", CTakumakuAIComponent)
Pointer_CActorComponent.add_option("CTargetComponent", CTargetComponent)
Pointer_CActorComponent.add_option("CTeleporterUsableComponent", CTeleporterUsableComponent)
Pointer_CActorComponent.add_option("CThermalDeviceComponent", CThermalDeviceComponent)
Pointer_CActorComponent.add_option("CThermalReactionComponent", CThermalReactionComponent)
Pointer_CActorComponent.add_option("CThermalRoomConnectionFX", CThermalRoomConnectionFX)
Pointer_CActorComponent.add_option("CThermalRoomFX", CThermalRoomFX)
Pointer_CActorComponent.add_option("CTimelineComponent", CTimelineComponent)
Pointer_CActorComponent.add_option("CTimerComponent", CTimerComponent)
Pointer_CActorComponent.add_option("CTotalRechargeComponent", CTotalRechargeComponent)
Pointer_CActorComponent.add_option("CTrainUsableComponent", CTrainUsableComponent)
Pointer_CActorComponent.add_option("CTrainUsableComponentCutScene", CTrainUsableComponentCutScene)
Pointer_CActorComponent.add_option("CTrainWithPortalUsableComponent", CTrainWithPortalUsableComponent)
Pointer_CActorComponent.add_option("CTriggerComponent", CTriggerComponent)
Pointer_CActorComponent.add_option("CTriggerNavMeshItemComponent", CTriggerNavMeshItemComponent)
Pointer_CActorComponent.add_option("CTunnelTrapMorphballComponent", CTunnelTrapMorphballComponent)
Pointer_CActorComponent.add_option("CUnlockAreaSmartObjectComponent", CUnlockAreaSmartObjectComponent)
Pointer_CActorComponent.add_option("CUsableComponent", CUsableComponent)
Pointer_CActorComponent.add_option("CVideoManagerComponent", CVideoManagerComponent)
Pointer_CActorComponent.add_option("CVulkranAIComponent", CVulkranAIComponent)
Pointer_CActorComponent.add_option("CVulkranMagmaBallMovementComponent", CVulkranMagmaBallMovementComponent)
Pointer_CActorComponent.add_option("CWarLotusAIComponent", CWarLotusAIComponent)
Pointer_CActorComponent.add_option("CWaterNozzleComponent", CWaterNozzleComponent)
Pointer_CActorComponent.add_option("CWaterPlatformUsableComponent", CWaterPlatformUsableComponent)
Pointer_CActorComponent.add_option("CWaterPoolComponent", CWaterPoolComponent)
Pointer_CActorComponent.add_option("CWaterTriggerChangeComponent", CWaterTriggerChangeComponent)
Pointer_CActorComponent.add_option("CWeaponMovement", CWeaponMovement)
Pointer_CActorComponent.add_option("CWeightActivableMovablePlatformComponent", CWeightActivableMovablePlatformComponent)
Pointer_CActorComponent.add_option("CWeightActivablePropComponent", CWeightActivablePropComponent)
Pointer_CActorComponent.add_option("CWeightActivatedPlatformSmartObjectComponent", CWeightActivatedPlatformSmartObjectComponent)
Pointer_CActorComponent.add_option("CWorldGraph", CWorldGraph)
Pointer_CActorComponent.add_option("CXParasiteAIComponent", CXParasiteAIComponent)
Pointer_CActorComponent.add_option("CXParasiteDropComponent", CXParasiteDropComponent)
Pointer_CActorComponent.add_option("CYamplotXAIComponent", CYamplotXAIComponent)

Pointer_CCentralUnitWeightedEdges.add_option("CCentralUnitWeightedEdges", CCentralUnitWeightedEdges)

Pointer_CEmmyAutoForbiddenEdgesDef.add_option("CEmmyAutoForbiddenEdgesDef", CEmmyAutoForbiddenEdgesDef)

Pointer_CEmmyAutoGlobalSmartLinkDef.add_option("CEmmyAutoGlobalSmartLinkDef", CEmmyAutoGlobalSmartLinkDef)

Pointer_CEmmyOverrideDeathPositionDef.add_option("CEmmyOverrideDeathPositionDef", CEmmyOverrideDeathPositionDef)

Pointer_CEnvironmentData_SAmbient.add_option("CEnvironmentData::SAmbient", CEnvironmentData_SAmbient)

Pointer_CEnvironmentData_SBloom.add_option("CEnvironmentData::SBloom", CEnvironmentData_SBloom)

Pointer_CEnvironmentData_SCubeMap.add_option("CEnvironmentData::SCubeMap", CEnvironmentData_SCubeMap)

Pointer_CEnvironmentData_SDepthTint.add_option("CEnvironmentData::SDepthTint", CEnvironmentData_SDepthTint)

Pointer_CEnvironmentData_SFog.add_option("CEnvironmentData::SFog", CEnvironmentData_SFog)

Pointer_CEnvironmentData_SHemisphericalLight.add_option("CEnvironmentData::SHemisphericalLight", CEnvironmentData_SHemisphericalLight)

Pointer_CEnvironmentData_SIBLAttenuation.add_option("CEnvironmentData::SIBLAttenuation", CEnvironmentData_SIBLAttenuation)

Pointer_CEnvironmentData_SMaterialTint.add_option("CEnvironmentData::SMaterialTint", CEnvironmentData_SMaterialTint)

Pointer_CEnvironmentData_SPlayerLight.add_option("CEnvironmentData::SPlayerLight", CEnvironmentData_SPlayerLight)

Pointer_CEnvironmentData_SSSAO.add_option("CEnvironmentData::SSSAO", CEnvironmentData_SSSAO)

Pointer_CEnvironmentData_SToneMapping.add_option("CEnvironmentData::SToneMapping", CEnvironmentData_SToneMapping)

Pointer_CEnvironmentData_SVerticalFog.add_option("CEnvironmentData::SVerticalFog", CEnvironmentData_SVerticalFog)

Pointer_CEnvironmentManager.add_option("CEnvironmentManager", CEnvironmentManager)

Pointer_CEnvironmentMusicPresets.add_option("CEnvironmentMusicPresets", CEnvironmentMusicPresets)

Pointer_CEnvironmentSoundPresets.add_option("CEnvironmentSoundPresets", CEnvironmentSoundPresets)

Pointer_CEnvironmentVisualPresets.add_option("CEnvironmentVisualPresets", CEnvironmentVisualPresets)

Pointer_CLogicCamera.add_option("CLogicCamera", CLogicCamera)

Pointer_CScenario.add_option("CScenario", CScenario)

Pointer_CSubAreaManager.add_option("CSubAreaManager", CSubAreaManager)

Pointer_CSubareaCharclassGroup.add_option("CSubareaCharclassGroup", CSubareaCharclassGroup)

Pointer_CSubareaInfo.add_option("CSubareaInfo", CSubareaInfo)

Pointer_CSubareaSetup.add_option("CSubareaSetup", CSubareaSetup)

Pointer_CTriggerComponent_SActivationCondition.add_option("CTriggerComponent::SActivationCondition", CTriggerComponent_SActivationCondition)

Pointer_CTriggerLogicAction.add_option("CTriggerLogicAction", CTriggerLogicAction)
Pointer_CTriggerLogicAction.add_option("CAllowCoolShinesparkLogicAction", CAllowCoolShinesparkLogicAction)
Pointer_CTriggerLogicAction.add_option("CCameraToRailLogicAction", CCameraToRailLogicAction)
Pointer_CTriggerLogicAction.add_option("CChangeSetupLogicAction", CChangeSetupLogicAction)
Pointer_CTriggerLogicAction.add_option("CChangeStateDoorsLogicAction", CChangeStateDoorsLogicAction)
Pointer_CTriggerLogicAction.add_option("CCheckCoolShinesparkSuccessfullyCompletedLogicAction", CCheckCoolShinesparkSuccessfullyCompletedLogicAction)
Pointer_CTriggerLogicAction.add_option("CCoolShinesparkMarkMinimapLogicAction", CCoolShinesparkMarkMinimapLogicAction)
Pointer_CTriggerLogicAction.add_option("CEmmyStateOverrideLogicAction", CEmmyStateOverrideLogicAction)
Pointer_CTriggerLogicAction.add_option("CForbiddenEdgesLogicAction", CForbiddenEdgesLogicAction)
Pointer_CTriggerLogicAction.add_option("CForceMovementLogicAction", CForceMovementLogicAction)
Pointer_CTriggerLogicAction.add_option("CFreeAimTutoLogicAction", CFreeAimTutoLogicAction)
Pointer_CTriggerLogicAction.add_option("CHoldPlayerDirectionOnSubAreaChangeLogicAction", CHoldPlayerDirectionOnSubAreaChangeLogicAction)
Pointer_CTriggerLogicAction.add_option("CIgnoreFloorSlideUpperBodySubmergedLogicAction", CIgnoreFloorSlideUpperBodySubmergedLogicAction)
Pointer_CTriggerLogicAction.add_option("CItemDestructionLogicAction", CItemDestructionLogicAction)
Pointer_CTriggerLogicAction.add_option("CLockRoomLogicAction", CLockRoomLogicAction)
Pointer_CTriggerLogicAction.add_option("CLuaCallsLogicAction", CLuaCallsLogicAction)
Pointer_CTriggerLogicAction.add_option("CMarkMinimapLogicAction", CMarkMinimapLogicAction)
Pointer_CTriggerLogicAction.add_option("CPerceptionModifierLogicAction", CPerceptionModifierLogicAction)
Pointer_CTriggerLogicAction.add_option("CSPBTutoLogicAction", CSPBTutoLogicAction)
Pointer_CTriggerLogicAction.add_option("CSPRTutoLogicAction", CSPRTutoLogicAction)
Pointer_CTriggerLogicAction.add_option("CSamusOverrideDistanceToBorderLogicAction", CSamusOverrideDistanceToBorderLogicAction)
Pointer_CTriggerLogicAction.add_option("CSaveGameFromEmmyDoorLogicAction", CSaveGameFromEmmyDoorLogicAction)
Pointer_CTriggerLogicAction.add_option("CSaveGameLogicAction", CSaveGameLogicAction)
Pointer_CTriggerLogicAction.add_option("CSaveGameToSnapshotLogicAction", CSaveGameToSnapshotLogicAction)
Pointer_CTriggerLogicAction.add_option("CSaveSnapshotToCheckpointLogicAction", CSaveSnapshotToCheckpointLogicAction)
Pointer_CTriggerLogicAction.add_option("CSetActorEnabledLogicAction", CSetActorEnabledLogicAction)
Pointer_CTriggerLogicAction.add_option("CShowPopUpCompositionLogicAction", CShowPopUpCompositionLogicAction)
Pointer_CTriggerLogicAction.add_option("CStartCentralUnitCombatLogicAction", CStartCentralUnitCombatLogicAction)
Pointer_CTriggerLogicAction.add_option("CSubareaTransitionTypeLogicAction", CSubareaTransitionTypeLogicAction)
Pointer_CTriggerLogicAction.add_option("CTutoEnterLogicAction", CTutoEnterLogicAction)
Pointer_CTriggerLogicAction.add_option("CTutoExitLogicAction", CTutoExitLogicAction)

Pointer_CXParasiteBehavior.add_option("CXParasiteBehavior", CXParasiteBehavior)
Pointer_CXParasiteBehavior.add_option("CXParasiteGoSpawnBehavior", CXParasiteGoSpawnBehavior)
Pointer_CXParasiteBehavior.add_option("CXParasiteGoTransformBehavior", CXParasiteGoTransformBehavior)
Pointer_CXParasiteBehavior.add_option("CXParasiteStayOnPlaceBehavior", CXParasiteStayOnPlaceBehavior)
Pointer_CXParasiteBehavior.add_option("CXParasiteWanderThenFleeBehavior", CXParasiteWanderThenFleeBehavior)

Pointer_base_global_CFilePathStrId.add_option("base::global::CFilePathStrId", base_global_CFilePathStrId)

Pointer_base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_.add_option("base::global::CRntSmallDictionary<base::global::CStrId, CActorComponent*>", base_global_CRntSmallDictionary_base_global_CStrId__CActorComponentPtr_)

Pointer_base_global_CRntVector_CEnvironmentData_SAmbientTransition_.add_option("base::global::CRntVector<CEnvironmentData::SAmbientTransition>", base_global_CRntVector_CEnvironmentData_SAmbientTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SBloomTransition_.add_option("base::global::CRntVector<CEnvironmentData::SBloomTransition>", base_global_CRntVector_CEnvironmentData_SBloomTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SCubeMapTransition_.add_option("base::global::CRntVector<CEnvironmentData::SCubeMapTransition>", base_global_CRntVector_CEnvironmentData_SCubeMapTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SDepthTintTransition_.add_option("base::global::CRntVector<CEnvironmentData::SDepthTintTransition>", base_global_CRntVector_CEnvironmentData_SDepthTintTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SFogTransition_.add_option("base::global::CRntVector<CEnvironmentData::SFogTransition>", base_global_CRntVector_CEnvironmentData_SFogTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_.add_option("base::global::CRntVector<CEnvironmentData::SHemisphericalLightTransition>", base_global_CRntVector_CEnvironmentData_SHemisphericalLightTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_.add_option("base::global::CRntVector<CEnvironmentData::SIBLAttenuationTransition>", base_global_CRntVector_CEnvironmentData_SIBLAttenuationTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_.add_option("base::global::CRntVector<CEnvironmentData::SMaterialTintTransition>", base_global_CRntVector_CEnvironmentData_SMaterialTintTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_.add_option("base::global::CRntVector<CEnvironmentData::SPlayerLightTransition>", base_global_CRntVector_CEnvironmentData_SPlayerLightTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SSSAOTransition_.add_option("base::global::CRntVector<CEnvironmentData::SSSAOTransition>", base_global_CRntVector_CEnvironmentData_SSSAOTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SToneMappingTransition_.add_option("base::global::CRntVector<CEnvironmentData::SToneMappingTransition>", base_global_CRntVector_CEnvironmentData_SToneMappingTransition_)

Pointer_base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_.add_option("base::global::CRntVector<CEnvironmentData::SVerticalFogTransition>", base_global_CRntVector_CEnvironmentData_SVerticalFogTransition_)

Pointer_base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__.add_option("base::global::CRntVector<std::unique_ptr<CSubareaCharclassGroup>>", base_global_CRntVector_std_unique_ptr_CSubareaCharclassGroup__)

Pointer_base_global_CRntVector_std_unique_ptr_CSubareaSetup__.add_option("base::global::CRntVector<std::unique_ptr<CSubareaSetup>>", base_global_CRntVector_std_unique_ptr_CSubareaSetup__)

Pointer_base_reflection_CTypedValue.add_option("base::global::CRntFile", base_global_CRntFile)

Pointer_game_logic_collision_CCollider.add_option("game::logic::collision::CCollider", game_logic_collision_CCollider)

Pointer_game_logic_collision_CShape.add_option("game::logic::collision::CShape", game_logic_collision_CShape)
Pointer_game_logic_collision_CShape.add_option("game::logic::collision::CAABoxShape2D", game_logic_collision_CAABoxShape2D)
Pointer_game_logic_collision_CShape.add_option("game::logic::collision::CCapsuleShape2D", game_logic_collision_CCapsuleShape2D)
Pointer_game_logic_collision_CShape.add_option("game::logic::collision::CCircleShape2D", game_logic_collision_CCircleShape2D)
Pointer_game_logic_collision_CShape.add_option("game::logic::collision::COBoxShape2D", game_logic_collision_COBoxShape2D)
Pointer_game_logic_collision_CShape.add_option("game::logic::collision::CPolygonCollectionShape", game_logic_collision_CPolygonCollectionShape)

