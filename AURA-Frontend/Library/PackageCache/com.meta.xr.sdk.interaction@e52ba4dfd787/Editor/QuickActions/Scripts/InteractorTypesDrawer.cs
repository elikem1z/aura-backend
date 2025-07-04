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

using UnityEditor;
using UnityEngine;
using System.Linq;
using System;

namespace Oculus.Interaction.Editor.QuickActions
{
    /// <summary>
    /// Draws a mask field for InteractorTypes, but ignoring the
    /// harcoded InteractorTypes.None and InteractorTypes.All in favor of the Unity ones;
    /// and all experimental values set beyonf InteractorTypes.All.
    /// </summary>
    [CustomPropertyDrawer(typeof(InteractorTypes))]
    public class InteractorTypesDrawer : PropertyDrawer
    {
        public override void OnGUI(Rect position, SerializedProperty property, GUIContent label)
        {
            int visibleValues = property.intValue & (int)InteractorTypes.All;
            InteractorTypes currentFlags = (InteractorTypes)Enum.ToObject(typeof(InteractorTypes), visibleValues);

            string[] options = Enum.GetValues(typeof(InteractorTypes))
                .Cast<InteractorTypes>()
                .Where(value => value > InteractorTypes.None && value < InteractorTypes.All)
                .Select(value => value.ToString()).ToArray();

            property.intValue = EditorGUI.MaskField(position, label, visibleValues, options);
        }
    }
}
