/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 * All rights reserved.
 *
 * Licensed under the Oculus SDK License Agreement (the "License");
 * you may not use the Oculus SDK except in compliance with the License,
 * which is provided at the time of installation or download, or which
 * otherwise accompanies this software in either electronic or hard copy form.
 *
 * You may obtain a copy of the License at
 *
 * https://developer.oculus.com/licenses/oculussdk/
 *
 * Unless required by applicable law or agreed to in writing, the Oculus SDK
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/************************************************************************************
 * Filename    :   MetaXRAudioSourceExperimentalFeatures.cs
 * Content     :   Extended Interface into the Meta XR Audio Plugin
 ***********************************************************************************/


using UnityEngine;
using System;
using System.Collections;
using System.Runtime.InteropServices;

/// \brief Component to extend the built-in AudioSource with Meta-specific, experimental features.
///
/// Adding this component to any game object that also has an AudioSource component allows specification of
/// Meta-specific experimental parameters to control how that audio source is rendered.
///
/// The public member variables of this class directly control the spatializer plug-in assigned to the accompaning
/// audio source. The spatializer plug-ins values are updated to the member variable values every call to
/// MetaXRAudioSourceExperimentalFeatures::Update().
///
/// To extend an AudioSource with Meta-specific, non-experimental features, use \ref MetaXRAudioSource.
[RequireComponent(typeof(MetaXRAudioSource))]
public class MetaXRAudioSourceExperimentalFeatures : MonoBehaviour
{
    private AudioSource source_;

    // Public
    [SerializeField]
    [Tooltip("How much of the HRTF EQ is applied to the sound. Interaural time delay (ITD) and interaural level differences (ILD) are kept the same.")]
    [Range(0.0f, 1.0f)]
    private float hrtfIntensity = 1.0f;
    /// \brief HRTF intensity for audio source [0.0, 1.0], Default = 1.0.
    ///
    /// HRTF intensity provides a control to fade between rendering the direct sound using a perceptually-guided
    /// panning law (when this parameter is 0.0) versus full HRTF convolution (when this parameter is 1.0). This can
    /// be useful to reduce what some users perceive as coloration caused by HRTF convolution at the expense of
    /// spatial localization accuracy of the listener.
    ///
    /// Note the interaural time delay (ITD) and interaural level differences (ILD) are the same for any setting of
    /// HRTF intensity.
    public float HrtfIntensity
    {
        get
        {
            return hrtfIntensity;
        }
        set
        {
            hrtfIntensity = Mathf.Clamp(value, 0.0f, 1.0f);
        }
    }

    [SerializeField]
    [Tooltip("Used to increase the spatial audio emitter radius. Useful for sounds that come from a large area rather than a precise point. If increased too large, users may end up inside the radius if the sound source is too close.")]
    private float volumetricRadius = 0.0f;
    /// \brief Volumetric radius (in meters) of the sound source. [0,+Inf), Default = 0m.
    ///
    /// This parameter simulates sound sources that are no just points, but whose radiator occupies a volume of space.
    /// Note, if increased too large, users may end up inside the radius if the sound source is too close.
    public float VolumetricRadius
    {
        get
        {
            return volumetricRadius;
        }
        set
        {
            volumetricRadius = Mathf.Max(value, 0.0f);
        }
    }

    [SerializeField]
    [Tooltip("Additional gain applied to early reflections for this audio source only")]
    [Range(-60.0f, 20.0f)]
    private float earlyReflectionsSendDb = 0.0f;
    /// \brief Additional gain applied to early reflections for this audio source only. [-60dB, 20dB], Default = 0dB.
    ///
    /// The direct sound and late reverberation levels are not affected by this setting. This setting only applies if
    /// MetaXRAudioSource#EnableAcoustics is enabled.
    ///
    /// \see MetaXRAudioSource#EnableAcoustics for enabling/disabling acoustics.
    /// \see MetaXRAudioSource#GainBoostDb for a gain that simultaneously applies to the direct sound, early reflections, and late reverberation.
    /// \see MetaXRAudioSource#ReverbSendDb for a gain that applies only to the late reverberation.
    public float EarlyReflectionsSendDb
    {
        get
        {
            return earlyReflectionsSendDb;
        }
        set
        {
            earlyReflectionsSendDb = Mathf.Clamp(value, -60.0f, 20.0f);
        }
    }

    [SerializeField]
    [Tooltip("Adjust how much the direct-to-reverberant ratio increases with distance")]
    [Range(0.0f, 1.0f)]
    private float reverbReach = 0.5f;
    /// \brief Adjust the affect of distance on the late reverberation level. [0, 1], Default = 0.5.
    ///
    /// When 0, moving away from the source will attenuate the late reverberation in the same way as the direct sound is attenuated with distance.
    /// When 1, moving away from the source will attenuate the late reverberation to a lesser degree than the direct sound. This means that the direct-to-reverberant ratio of the audio source will change, and moving further away will make the object sound "wetter".
    /// 0.5 is the most realistic setting and the default.
    public float ReverbReach
    {
        get
        {
            return reverbReach;
        }
        set
        {
            reverbReach = Mathf.Clamp(value, 0.0f, 1.0f);
        }
    }

    [SerializeField]
    [Tooltip("Adjust how much the direct-to-reverberant ratio increases with distance")]
    [Range(0.0f, 1.0f)]
    private float occlusionIntensity = 1.0f;
    /// \brief Adjust how much occlusion to apply with 1 being complete occlusion and 0 being no occlusion  [0, 1], Default = 1.0f.
    ///
    /// When 0, the source will sound as if there is no occlusion even if there is an obstruction.
    /// When 1, no direct sound will propagate from the source if there is obstruction between the source and listener.
    /// 1 is the most realistic setting and the default.
    public float OcclusionIntensity
    {
        get
        {
            return occlusionIntensity;
        }
        set
        {
            occlusionIntensity = Mathf.Clamp(value, 0.0f, 1.0f);
        }
    }

    public enum DirectivityPatternType
    {
        None, ///< No directivity applied. Omnidirectional radiation pattern. Effectively disables any directivity processing.
        HumanVoice, ///< Directivity pattern that most closely matches the radiation pattern of the human mouth/head.
    }

    [SerializeField]
    [Tooltip("Intensity controller for Directvity , Value of 1 will apply full directivity")]
    [Range(0.0f, 1.0f)]
    private float directivityIntensity = 1.0f;
    /// \brief Intensity controller for Directivity, [0, 1], Default = 1.0.
    ///
    /// When 0, even if directivity is enabled and a non-omnidirection pattern is selected, the directivity will be
    /// that of an omnidirectional radiator. When 1, the directivity pattern selected will be fully applied.
    /// Intermediate values allow the user to crossfade between the two (i.e. smoothly transition from an
    /// omnidirectional radiator to the chosen directivity pattern).
    ///
    /// \see DirectivityPatternType for the available directivity patterns.
    /// \see DirectivityPattern for controlling which pattern is applied to this audio source.
    public float DirectivityIntensity
    {
        get
        {
            return directivityIntensity;
        }
        set
        {
            directivityIntensity = Mathf.Clamp(value, 0.0f, 1.0f);
        }
    }

    [SerializeField]
    [Tooltip("Option for human voice directivity pattern that makes this sound more muffled when the source is facing away from listener")]
    private DirectivityPatternType directivityPattern = DirectivityPatternType.None;
    /// \brief Select various directivity patterns to apply to this audio source.
    ///
    /// \see DirectivityPatternType for the available directivity patterns.
    /// \see DirectivityPattern for controlling which pattern is applied to this audio source.
    public DirectivityPatternType DirectivityPattern
    {
        get
        {
            return directivityPattern;
        }
        set
        {
            directivityPattern = value;
        }
    }

    [SerializeField]
    [Tooltip("This switch can disable direct sound propagation, so only late reverberations is heard from this source")]
    private bool directSoundEnabled = true;
    /// \brief Enable/disable the direct sound and early reflections for an audio source.
    ///
    /// When enabled, the audio source will have it's direct sound rendered in addition to early reflections and late reverberations (assuming MetaXRAudioSource#EnableAcoustics is enabled).
    /// When disabled, only the late reverberation is rendered (again, assuming MetaXRAudioSource#EnableAcoustics is enabled, otherwise the source will be silent).
    public bool DirectSoundEnabled
    {
        get
        {
            return directSoundEnabled;
        }
        set
        {
            directSoundEnabled = value;
        }
    }

    [SerializeField]
    [Tooltip("This switch can disable direct sound propagation, so only late reverberations is heard from this source")]
    private bool mediumAbsorption = true;
    /// \brief If enabled and using Acoustic Ray Tracing, medium absorption will be applied to the source over distance
    ///
    /// This control only applies when Acoustic Ray Tracing is being used.
    /// When enabled, the audio source will apply frequency specific attenuation over distance as a result of the medium the sound travels through (air for example).
    /// When disabled, no medium specific frequency attenuation will be applied over distance.
    public bool MediumAbsorption
    {
        get
        {
            return mediumAbsorption;
        }
        set
        {
            mediumAbsorption = value;
        }
    }

    private void OnValidate()
    {
        volumetricRadius = Mathf.Max(volumetricRadius, 0.0f);
    }

    void Awake()
    {
        // We might iterate through multiple sources / game object
        source_ = GetComponent<AudioSource>();
        UpdateParameters();
    }

    void Update()
    {
        // We might iterate through multiple sources / game object
        if (source_ == null)
        {
            source_ = GetComponent<AudioSource>();
            if (source_ == null)
            {
                return;
            }
        }

        UpdateParameters();
    }

    /// \brief Sync all the member variables of this class with the spatializer plug-in instance associated with this sound source.
    ///
    /// This function should be called during every call to Update and so there should be no need to call this
    /// explicitly unless you want to force sync the spatializer instance's parameters with this component.
    public void UpdateParameters()
    {
        source_.SetSpatializerFloat((int)MetaXRAudioSource.NativeParameterIndex.P_HRTF_INTENSITY, hrtfIntensity);
        source_.SetSpatializerFloat((int)MetaXRAudioSource.NativeParameterIndex.P_DIRECTIVITY_INTENSITY, directivityIntensity);
        source_.SetSpatializerFloat((int)MetaXRAudioSource.NativeParameterIndex.P_RADIUS, volumetricRadius);
        source_.SetSpatializerFloat((int)MetaXRAudioSource.NativeParameterIndex.P_REFLECTIONS_SEND, earlyReflectionsSendDb);
        source_.SetSpatializerFloat((int)MetaXRAudioSource.NativeParameterIndex.P_DIRECTIVITY_ENABLED, directivityPattern == DirectivityPatternType.None ? 0.0f : 1.0f);
        source_.SetSpatializerFloat((int)MetaXRAudioSource.NativeParameterIndex.P_REVERB_REACH, reverbReach);
        source_.SetSpatializerFloat((int)MetaXRAudioSource.NativeParameterIndex.P_DIRECT_ENABLED, directSoundEnabled ? 1.0f : 0.0f);
        source_.SetSpatializerFloat((int)MetaXRAudioSource.NativeParameterIndex.P_OCCLUSION_INTENSITY, occlusionIntensity);
        source_.SetSpatializerFloat((int)MetaXRAudioSource.NativeParameterIndex.P_MEDIUM_ABSORPTION, mediumAbsorption ? 1.0f : 0.0f);
    }

    // Import functions
    [DllImport(MetaXRAudioNativeInterface.UnityNativeInterface.binaryName)]
    private static extern void MetaXRAudio_GetGlobalRoomReflectionValues(ref bool reflOn, ref bool reverbOn,
        ref float width, ref float height, ref float length);
}
