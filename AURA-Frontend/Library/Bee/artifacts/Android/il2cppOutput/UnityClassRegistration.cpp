extern "C" void RegisterStaticallyLinkedModulesGranular()
{
	void RegisterModule_SharedInternals();
	RegisterModule_SharedInternals();

	void RegisterModule_Core();
	RegisterModule_Core();

	void RegisterModule_AI();
	RegisterModule_AI();

	void RegisterModule_AndroidJNI();
	RegisterModule_AndroidJNI();

	void RegisterModule_Animation();
	RegisterModule_Animation();

	void RegisterModule_AssetBundle();
	RegisterModule_AssetBundle();

	void RegisterModule_Audio();
	RegisterModule_Audio();

	void RegisterModule_GraphicsStateCollectionSerializer();
	RegisterModule_GraphicsStateCollectionSerializer();

	void RegisterModule_HierarchyCore();
	RegisterModule_HierarchyCore();

	void RegisterModule_HotReload();
	RegisterModule_HotReload();

	void RegisterModule_IMGUI();
	RegisterModule_IMGUI();

	void RegisterModule_ImageConversion();
	RegisterModule_ImageConversion();

	void RegisterModule_Input();
	RegisterModule_Input();

	void RegisterModule_InputLegacy();
	RegisterModule_InputLegacy();

	void RegisterModule_InputForUI();
	RegisterModule_InputForUI();

	void RegisterModule_JSONSerialize();
	RegisterModule_JSONSerialize();

	void RegisterModule_Physics();
	RegisterModule_Physics();

	void RegisterModule_Physics2D();
	RegisterModule_Physics2D();

	void RegisterModule_Properties();
	RegisterModule_Properties();

	void RegisterModule_RuntimeInitializeOnLoadManagerInitializer();
	RegisterModule_RuntimeInitializeOnLoadManagerInitializer();

	void RegisterModule_Subsystems();
	RegisterModule_Subsystems();

	void RegisterModule_TLS();
	RegisterModule_TLS();

	void RegisterModule_Terrain();
	RegisterModule_Terrain();

	void RegisterModule_TextRendering();
	RegisterModule_TextRendering();

	void RegisterModule_TextCoreFontEngine();
	RegisterModule_TextCoreFontEngine();

	void RegisterModule_TextCoreTextEngine();
	RegisterModule_TextCoreTextEngine();

	void RegisterModule_UI();
	RegisterModule_UI();

	void RegisterModule_UIElements();
	RegisterModule_UIElements();

	void RegisterModule_UnityAnalyticsCommon();
	RegisterModule_UnityAnalyticsCommon();

	void RegisterModule_UnityConnect();
	RegisterModule_UnityConnect();

	void RegisterModule_UnityWebRequest();
	RegisterModule_UnityWebRequest();

	void RegisterModule_UnityAnalytics();
	RegisterModule_UnityAnalytics();

	void RegisterModule_UnityWebRequestAudio();
	RegisterModule_UnityWebRequestAudio();

	void RegisterModule_XR();
	RegisterModule_XR();

	void RegisterModule_VR();
	RegisterModule_VR();

}

template <typename T> void RegisterUnityClass(const char*);
template <typename T> void RegisterStrippedType(int, const char*, const char*);

void InvokeRegisterStaticallyLinkedModuleClasses()
{
	// Do nothing (we're in stripping mode)
}

class NavMeshAgent; template <> void RegisterUnityClass<NavMeshAgent>(const char*);
class NavMeshData; template <> void RegisterUnityClass<NavMeshData>(const char*);
class NavMeshObstacle; template <> void RegisterUnityClass<NavMeshObstacle>(const char*);
class NavMeshProjectSettings; template <> void RegisterUnityClass<NavMeshProjectSettings>(const char*);
class NavMeshSettings; template <> void RegisterUnityClass<NavMeshSettings>(const char*);
class Animator; template <> void RegisterUnityClass<Animator>(const char*);
class AnimatorController; template <> void RegisterUnityClass<AnimatorController>(const char*);
class AnimatorOverrideController; template <> void RegisterUnityClass<AnimatorOverrideController>(const char*);
class Avatar; template <> void RegisterUnityClass<Avatar>(const char*);
class RuntimeAnimatorController; template <> void RegisterUnityClass<RuntimeAnimatorController>(const char*);
class AssetBundle; template <> void RegisterUnityClass<AssetBundle>(const char*);
class AudioBehaviour; template <> void RegisterUnityClass<AudioBehaviour>(const char*);
class AudioClip; template <> void RegisterUnityClass<AudioClip>(const char*);
class AudioListener; template <> void RegisterUnityClass<AudioListener>(const char*);
class AudioManager; template <> void RegisterUnityClass<AudioManager>(const char*);
class AudioResource; template <> void RegisterUnityClass<AudioResource>(const char*);
class AudioSource; template <> void RegisterUnityClass<AudioSource>(const char*);
class SampleClip; template <> void RegisterUnityClass<SampleClip>(const char*);
class Behaviour; template <> void RegisterUnityClass<Behaviour>(const char*);
class BuildSettings; template <> void RegisterUnityClass<BuildSettings>(const char*);
class Camera; template <> void RegisterUnityClass<Camera>(const char*);
namespace Unity { class Component; } template <> void RegisterUnityClass<Unity::Component>(const char*);
class ComputeShader; template <> void RegisterUnityClass<ComputeShader>(const char*);
class Cubemap; template <> void RegisterUnityClass<Cubemap>(const char*);
class CubemapArray; template <> void RegisterUnityClass<CubemapArray>(const char*);
class DelayedCallManager; template <> void RegisterUnityClass<DelayedCallManager>(const char*);
class EditorExtension; template <> void RegisterUnityClass<EditorExtension>(const char*);
class GameManager; template <> void RegisterUnityClass<GameManager>(const char*);
class GameObject; template <> void RegisterUnityClass<GameObject>(const char*);
class GlobalGameManager; template <> void RegisterUnityClass<GlobalGameManager>(const char*);
class GraphicsSettings; template <> void RegisterUnityClass<GraphicsSettings>(const char*);
class InputManager; template <> void RegisterUnityClass<InputManager>(const char*);
class LODGroup; template <> void RegisterUnityClass<LODGroup>(const char*);
class LevelGameManager; template <> void RegisterUnityClass<LevelGameManager>(const char*);
class Light; template <> void RegisterUnityClass<Light>(const char*);
class LightProbeProxyVolume; template <> void RegisterUnityClass<LightProbeProxyVolume>(const char*);
class LightProbes; template <> void RegisterUnityClass<LightProbes>(const char*);
class LightingSettings; template <> void RegisterUnityClass<LightingSettings>(const char*);
class LightmapSettings; template <> void RegisterUnityClass<LightmapSettings>(const char*);
class LineRenderer; template <> void RegisterUnityClass<LineRenderer>(const char*);
class LowerResBlitTexture; template <> void RegisterUnityClass<LowerResBlitTexture>(const char*);
class Material; template <> void RegisterUnityClass<Material>(const char*);
class Mesh; template <> void RegisterUnityClass<Mesh>(const char*);
class MeshFilter; template <> void RegisterUnityClass<MeshFilter>(const char*);
class MeshRenderer; template <> void RegisterUnityClass<MeshRenderer>(const char*);
class MonoBehaviour; template <> void RegisterUnityClass<MonoBehaviour>(const char*);
class MonoManager; template <> void RegisterUnityClass<MonoManager>(const char*);
class MonoScript; template <> void RegisterUnityClass<MonoScript>(const char*);
class NamedObject; template <> void RegisterUnityClass<NamedObject>(const char*);
class Object; template <> void RegisterUnityClass<Object>(const char*);
class PlayerSettings; template <> void RegisterUnityClass<PlayerSettings>(const char*);
class PreloadData; template <> void RegisterUnityClass<PreloadData>(const char*);
class QualitySettings; template <> void RegisterUnityClass<QualitySettings>(const char*);
namespace UI { class RectTransform; } template <> void RegisterUnityClass<UI::RectTransform>(const char*);
class ReflectionProbe; template <> void RegisterUnityClass<ReflectionProbe>(const char*);
class RenderSettings; template <> void RegisterUnityClass<RenderSettings>(const char*);
class RenderTexture; template <> void RegisterUnityClass<RenderTexture>(const char*);
class Renderer; template <> void RegisterUnityClass<Renderer>(const char*);
class ResourceManager; template <> void RegisterUnityClass<ResourceManager>(const char*);
class RuntimeInitializeOnLoadManager; template <> void RegisterUnityClass<RuntimeInitializeOnLoadManager>(const char*);
class Shader; template <> void RegisterUnityClass<Shader>(const char*);
class ShaderNameRegistry; template <> void RegisterUnityClass<ShaderNameRegistry>(const char*);
class SkinnedMeshRenderer; template <> void RegisterUnityClass<SkinnedMeshRenderer>(const char*);
class SortingGroup; template <> void RegisterUnityClass<SortingGroup>(const char*);
class Sprite; template <> void RegisterUnityClass<Sprite>(const char*);
class SpriteAtlas; template <> void RegisterUnityClass<SpriteAtlas>(const char*);
class SpriteRenderer; template <> void RegisterUnityClass<SpriteRenderer>(const char*);
class TagManager; template <> void RegisterUnityClass<TagManager>(const char*);
class TextAsset; template <> void RegisterUnityClass<TextAsset>(const char*);
class Texture; template <> void RegisterUnityClass<Texture>(const char*);
class Texture2D; template <> void RegisterUnityClass<Texture2D>(const char*);
class Texture2DArray; template <> void RegisterUnityClass<Texture2DArray>(const char*);
class Texture3D; template <> void RegisterUnityClass<Texture3D>(const char*);
class TimeManager; template <> void RegisterUnityClass<TimeManager>(const char*);
class Transform; template <> void RegisterUnityClass<Transform>(const char*);
class BoxCollider; template <> void RegisterUnityClass<BoxCollider>(const char*);
class CapsuleCollider; template <> void RegisterUnityClass<CapsuleCollider>(const char*);
class CharacterController; template <> void RegisterUnityClass<CharacterController>(const char*);
class Collider; template <> void RegisterUnityClass<Collider>(const char*);
namespace Unity { class ConfigurableJoint; } template <> void RegisterUnityClass<Unity::ConfigurableJoint>(const char*);
namespace Unity { class FixedJoint; } template <> void RegisterUnityClass<Unity::FixedJoint>(const char*);
namespace Unity { class Joint; } template <> void RegisterUnityClass<Unity::Joint>(const char*);
class MeshCollider; template <> void RegisterUnityClass<MeshCollider>(const char*);
class PhysicsManager; template <> void RegisterUnityClass<PhysicsManager>(const char*);
class PhysicsMaterial; template <> void RegisterUnityClass<PhysicsMaterial>(const char*);
class Rigidbody; template <> void RegisterUnityClass<Rigidbody>(const char*);
class SphereCollider; template <> void RegisterUnityClass<SphereCollider>(const char*);
class Physics2DSettings; template <> void RegisterUnityClass<Physics2DSettings>(const char*);
class Terrain; template <> void RegisterUnityClass<Terrain>(const char*);
class TerrainData; template <> void RegisterUnityClass<TerrainData>(const char*);
namespace TextRendering { class Font; } template <> void RegisterUnityClass<TextRendering::Font>(const char*);
namespace UI { class Canvas; } template <> void RegisterUnityClass<UI::Canvas>(const char*);
namespace UI { class CanvasGroup; } template <> void RegisterUnityClass<UI::CanvasGroup>(const char*);
namespace UI { class CanvasRenderer; } template <> void RegisterUnityClass<UI::CanvasRenderer>(const char*);
class UIRenderer; template <> void RegisterUnityClass<UIRenderer>(const char*);

void RegisterAllClasses()
{
void RegisterBuiltinTypes();
RegisterBuiltinTypes();
	//Total: 95 non stripped classes
	//0. NavMeshAgent
	RegisterUnityClass<NavMeshAgent>("AI");
	//1. NavMeshData
	RegisterUnityClass<NavMeshData>("AI");
	//2. NavMeshObstacle
	RegisterUnityClass<NavMeshObstacle>("AI");
	//3. NavMeshProjectSettings
	RegisterUnityClass<NavMeshProjectSettings>("AI");
	//4. NavMeshSettings
	RegisterUnityClass<NavMeshSettings>("AI");
	//5. Animator
	RegisterUnityClass<Animator>("Animation");
	//6. AnimatorController
	RegisterUnityClass<AnimatorController>("Animation");
	//7. AnimatorOverrideController
	RegisterUnityClass<AnimatorOverrideController>("Animation");
	//8. Avatar
	RegisterUnityClass<Avatar>("Animation");
	//9. RuntimeAnimatorController
	RegisterUnityClass<RuntimeAnimatorController>("Animation");
	//10. AssetBundle
	RegisterUnityClass<AssetBundle>("AssetBundle");
	//11. AudioBehaviour
	RegisterUnityClass<AudioBehaviour>("Audio");
	//12. AudioClip
	RegisterUnityClass<AudioClip>("Audio");
	//13. AudioListener
	RegisterUnityClass<AudioListener>("Audio");
	//14. AudioManager
	RegisterUnityClass<AudioManager>("Audio");
	//15. AudioResource
	RegisterUnityClass<AudioResource>("Audio");
	//16. AudioSource
	RegisterUnityClass<AudioSource>("Audio");
	//17. SampleClip
	RegisterUnityClass<SampleClip>("Audio");
	//18. Behaviour
	RegisterUnityClass<Behaviour>("Core");
	//19. BuildSettings
	RegisterUnityClass<BuildSettings>("Core");
	//20. Camera
	RegisterUnityClass<Camera>("Core");
	//21. Component
	RegisterUnityClass<Unity::Component>("Core");
	//22. ComputeShader
	RegisterUnityClass<ComputeShader>("Core");
	//23. Cubemap
	RegisterUnityClass<Cubemap>("Core");
	//24. CubemapArray
	RegisterUnityClass<CubemapArray>("Core");
	//25. DelayedCallManager
	RegisterUnityClass<DelayedCallManager>("Core");
	//26. EditorExtension
	RegisterUnityClass<EditorExtension>("Core");
	//27. GameManager
	RegisterUnityClass<GameManager>("Core");
	//28. GameObject
	RegisterUnityClass<GameObject>("Core");
	//29. GlobalGameManager
	RegisterUnityClass<GlobalGameManager>("Core");
	//30. GraphicsSettings
	RegisterUnityClass<GraphicsSettings>("Core");
	//31. InputManager
	RegisterUnityClass<InputManager>("Core");
	//32. LODGroup
	RegisterUnityClass<LODGroup>("Core");
	//33. LevelGameManager
	RegisterUnityClass<LevelGameManager>("Core");
	//34. Light
	RegisterUnityClass<Light>("Core");
	//35. LightProbeProxyVolume
	RegisterUnityClass<LightProbeProxyVolume>("Core");
	//36. LightProbes
	RegisterUnityClass<LightProbes>("Core");
	//37. LightingSettings
	RegisterUnityClass<LightingSettings>("Core");
	//38. LightmapSettings
	RegisterUnityClass<LightmapSettings>("Core");
	//39. LineRenderer
	RegisterUnityClass<LineRenderer>("Core");
	//40. LowerResBlitTexture
	RegisterUnityClass<LowerResBlitTexture>("Core");
	//41. Material
	RegisterUnityClass<Material>("Core");
	//42. Mesh
	RegisterUnityClass<Mesh>("Core");
	//43. MeshFilter
	RegisterUnityClass<MeshFilter>("Core");
	//44. MeshRenderer
	RegisterUnityClass<MeshRenderer>("Core");
	//45. MonoBehaviour
	RegisterUnityClass<MonoBehaviour>("Core");
	//46. MonoManager
	RegisterUnityClass<MonoManager>("Core");
	//47. MonoScript
	RegisterUnityClass<MonoScript>("Core");
	//48. NamedObject
	RegisterUnityClass<NamedObject>("Core");
	//49. Object
	//Skipping Object
	//50. PlayerSettings
	RegisterUnityClass<PlayerSettings>("Core");
	//51. PreloadData
	RegisterUnityClass<PreloadData>("Core");
	//52. QualitySettings
	RegisterUnityClass<QualitySettings>("Core");
	//53. RectTransform
	RegisterUnityClass<UI::RectTransform>("Core");
	//54. ReflectionProbe
	RegisterUnityClass<ReflectionProbe>("Core");
	//55. RenderSettings
	RegisterUnityClass<RenderSettings>("Core");
	//56. RenderTexture
	RegisterUnityClass<RenderTexture>("Core");
	//57. Renderer
	RegisterUnityClass<Renderer>("Core");
	//58. ResourceManager
	RegisterUnityClass<ResourceManager>("Core");
	//59. RuntimeInitializeOnLoadManager
	RegisterUnityClass<RuntimeInitializeOnLoadManager>("Core");
	//60. Shader
	RegisterUnityClass<Shader>("Core");
	//61. ShaderNameRegistry
	RegisterUnityClass<ShaderNameRegistry>("Core");
	//62. SkinnedMeshRenderer
	RegisterUnityClass<SkinnedMeshRenderer>("Core");
	//63. SortingGroup
	RegisterUnityClass<SortingGroup>("Core");
	//64. Sprite
	RegisterUnityClass<Sprite>("Core");
	//65. SpriteAtlas
	RegisterUnityClass<SpriteAtlas>("Core");
	//66. SpriteRenderer
	RegisterUnityClass<SpriteRenderer>("Core");
	//67. TagManager
	RegisterUnityClass<TagManager>("Core");
	//68. TextAsset
	RegisterUnityClass<TextAsset>("Core");
	//69. Texture
	RegisterUnityClass<Texture>("Core");
	//70. Texture2D
	RegisterUnityClass<Texture2D>("Core");
	//71. Texture2DArray
	RegisterUnityClass<Texture2DArray>("Core");
	//72. Texture3D
	RegisterUnityClass<Texture3D>("Core");
	//73. TimeManager
	RegisterUnityClass<TimeManager>("Core");
	//74. Transform
	RegisterUnityClass<Transform>("Core");
	//75. BoxCollider
	RegisterUnityClass<BoxCollider>("Physics");
	//76. CapsuleCollider
	RegisterUnityClass<CapsuleCollider>("Physics");
	//77. CharacterController
	RegisterUnityClass<CharacterController>("Physics");
	//78. Collider
	RegisterUnityClass<Collider>("Physics");
	//79. ConfigurableJoint
	RegisterUnityClass<Unity::ConfigurableJoint>("Physics");
	//80. FixedJoint
	RegisterUnityClass<Unity::FixedJoint>("Physics");
	//81. Joint
	RegisterUnityClass<Unity::Joint>("Physics");
	//82. MeshCollider
	RegisterUnityClass<MeshCollider>("Physics");
	//83. PhysicsManager
	RegisterUnityClass<PhysicsManager>("Physics");
	//84. PhysicsMaterial
	RegisterUnityClass<PhysicsMaterial>("Physics");
	//85. Rigidbody
	RegisterUnityClass<Rigidbody>("Physics");
	//86. SphereCollider
	RegisterUnityClass<SphereCollider>("Physics");
	//87. Physics2DSettings
	RegisterUnityClass<Physics2DSettings>("Physics2D");
	//88. Terrain
	RegisterUnityClass<Terrain>("Terrain");
	//89. TerrainData
	RegisterUnityClass<TerrainData>("Terrain");
	//90. Font
	RegisterUnityClass<TextRendering::Font>("TextRendering");
	//91. Canvas
	RegisterUnityClass<UI::Canvas>("UI");
	//92. CanvasGroup
	RegisterUnityClass<UI::CanvasGroup>("UI");
	//93. CanvasRenderer
	RegisterUnityClass<UI::CanvasRenderer>("UI");
	//94. UIRenderer
	RegisterUnityClass<UIRenderer>("UIElements");

}
