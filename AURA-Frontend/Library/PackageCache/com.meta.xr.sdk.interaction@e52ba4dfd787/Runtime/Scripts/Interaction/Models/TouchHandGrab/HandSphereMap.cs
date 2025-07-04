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

using Oculus.Interaction.Input;
using System.Collections.Generic;
using UnityEngine;

namespace Oculus.Interaction
{
    /// <summary>
    /// Generate a mapping of joints to spheres from a HandPrefabDataSource
    /// that has a set of transforms representing sphere positions and radii.
    /// </summary>
    public class HandSphereMap : MonoBehaviour, IHandSphereMap
    {
        [SerializeField]
        public FromHandPrefabDataSource _handPrefabDataSource;

        private readonly List<HandSphere>[] _sourceSphereMap = new List<HandSphere>[Constants.NUM_HAND_JOINTS];

        protected virtual void Awake()
        {
            for (int i = 0; i < (int)HandJointId.HandEnd; i++)
            {
                _sourceSphereMap[i] = new List<HandSphere>();
            }
        }

        protected virtual void Start()
        {
            for (int i = 0; i < (int)HandJointId.HandEnd; i++)
            {
                List<HandSphere> spheres = _sourceSphereMap[i];
                HandJointId joint = (HandJointId)i;
                Transform assocTransform = _handPrefabDataSource.GetTransformFor(joint);

                if (assocTransform == null)
                {
                    continue;
                }

                foreach (Transform t in assocTransform)
                {
                    if (t.name != "sphere"
                        || !t.gameObject.activeSelf)
                    {
                        continue;
                    }

                    Pose sphereOffset = t.GetPose(Space.Self);
                    Vector3 position = sphereOffset.position;
                    spheres.Add(new HandSphere(position, t.lossyScale.x * 0.5f, joint));
                    t.gameObject.SetActive(false);
                }
            }
        }

        public void GetSpheres(Handedness handedness, HandJointId jointId, Pose jointPose, float scale,
            List<HandSphere> spheres)
        {
            bool isMirror = handedness != _handPrefabDataSource.Handedness;

            int idx = (int)jointId;
            for (int j = 0; j < _sourceSphereMap[idx].Count; j++)
            {
                HandSphere sphere = _sourceSphereMap[idx][j];
                Vector3 jointOffset = sphere.Position * scale;
                if (isMirror)
                {
                    jointOffset = HandMirroring.Mirror(jointOffset);
                }
                Vector3 spherePosition = jointPose.position + jointPose.rotation * jointOffset;
                HandSphere target = new HandSphere(
                    spherePosition,
                    sphere.Radius * scale,
                    sphere.Joint);
                spheres.Add(target);
            }
        }

    }
}
