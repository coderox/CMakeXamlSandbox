cmake_minimum_required(VERSION 3.8)
project(CMakeSandbox)

if(MSVC_VERSION GREATER 1700)
  set(COMPILER_VERSION "12")
elseif(MSVC_VERSION GREATER 1600)
  set(COMPILER_VERSION "11")
endif()

#Enable folders grouping in IDE
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

#Add dependencies for client project
set(DEPENDENCIES_INCLUDE_DIRECTORIES "")
set(DEPENDENCIES_INCLUDE_RUNTIMES "")
add_subdirectory(dependencies)

message(STATUS "${DEPENDENCIES_INCLUDE_DIRECTORIES}")

set (APP_MANIFEST_NAME Package.appxmanifest)

set(EXE_NAME CMakeSandbox)
set(SHORT_NAME ${EXE_NAME})
set(PACKAGE_GUID "6515377e-dfd4-4cdb-80df-4e0326346efc")

configure_file(
    cmake/${APP_MANIFEST_NAME}
    ${CMAKE_CURRENT_BINARY_DIR}/${APP_MANIFEST_NAME}
    @ONLY
)

set(SOURCE_FILES
    source/App.xaml
    source/App.xaml.cpp
    source/App.xaml.h
    source/DirectXPage.xaml
    source/DirectXPage.xaml.cpp
    source/DirectXPage.xaml.h
    source/CMakeSandboxMain.cpp
    source/CMakeSandboxMain.h
    source/OpenGLES.cpp
    source/OpenGLES.h
    source/OpenGLESPage.xaml
    source/OpenGLESPage.xaml.cpp
    source/OpenGLESPage.xaml.h
    source/pch.cpp
    source/pch.h
)

set(COMMON_FILES
    source/Common/DeviceResources.cpp
    source/Common/DeviceResources.h
    source/Common/DirectXHelper.h
    source/Common/StepTimer.h
    source/Common/MathHelper.h
)

set(CONTENT_FILES
    source/Content/Sample3DSceneRenderer.cpp
    source/Content/SampleFpsTextRenderer.cpp
    source/Content/Sample3DSceneRenderer.h
    source/Content/SampleFpsTextRenderer.h
    source/Content/ShaderStructures.h
    source/Content/SimpleRenderer.h
    source/Content/SimpleRenderer.cpp
)

set(PIXELSHADER_FILES
  source/Content/SamplePixelShader.hlsl
)

set(VERTEXSHADER_FILES
  source/Content/SampleVertexShader.hlsl
)

set(CONTENT_FILES 
    ${CONTENT_FILES}
    ${PIXELSHADER_FILES} ${VERTEXSHADER_FILES}
)

set(ASSET_FILES ${ASSET_FILES}
    source/Assets/LockScreenLogo.scale-200.png
    source/Assets/SplashScreen.scale-200.png
    source/Assets/Square44x44Logo.scale-200.png
    source/Assets/Square44x44Logo.targetsize-24_altform-unplated.png
    source/Assets/Square150x150Logo.scale-200.png
    source/Assets/StoreLogo.png
    source/Assets/Wide310x150Logo.scale-200.png
)

set_property(SOURCE ${CONTENT_FILES} PROPERTY VS_DEPLOYMENT_CONTENT 1)
set_property(SOURCE ${ASSET_FILES} PROPERTY VS_DEPLOYMENT_CONTENT 1)
set_property(SOURCE ${ASSET_FILES} PROPERTY VS_DEPLOYMENT_LOCATION "Assets")
set_property(SOURCE ${DEBUG_CONTENT_FILES} PROPERTY VS_DEPLOYMENT_CONTENT $<CONFIG:Debug>)
set_property(SOURCE ${RELEASE_CONTENT_FILES} PROPERTY VS_DEPLOYMENT_CONTENT $<OR:$<CONFIG:Release>,$<CONFIG:RelWithDebInfo>,$<CONFIG:MinSizeRel>>)

set_property(SOURCE ${PIXELSHADER_FILES} PROPERTY VS_SHADER_TYPE Pixel)
set_property(SOURCE ${PIXELSHADER_FILES} PROPERTY VS_SHADER_ENTRYPOINT main)
set_property(SOURCE ${PIXELSHADER_FILES} PROPERTY VS_SHADER_MODEL 4.0_level_9_3)
set_property(SOURCE ${PIXELSHADER_FILES} PROPERTY VS_SHADER_FLAGS "/DFLAGS_ADDED /Fh \"$(OutDir)%(Filename).h\"")

set_property(SOURCE ${VERTEXSHADER_FILES} PROPERTY VS_SHADER_TYPE Vertex)
set_property(SOURCE ${VERTEXSHADER_FILES} PROPERTY VS_SHADER_ENTRYPOINT main)
set_property(SOURCE ${VERTEXSHADER_FILES} PROPERTY VS_SHADER_MODEL 4.0_level_9_3)
set_property(SOURCE ${VERTEXSHADER_FILES} PROPERTY VS_SHADER_FLAGS "/DFLAGS_ADDED /Fh \"$(OutDir)%(Filename).h\"")

set_property(SOURCE "source/App.xaml" PROPERTY VS_XAML_TYPE "ApplicationDefinition") 

source_group("Common" FILES ${COMMON_FILES})
source_group("Content" FILES ${CONTENT_FILES})
source_group("Assets" FILES ${ASSET_FILES})

add_executable(${EXE_NAME} WIN32 ${SOURCE_FILES} ${COMMON_FILES} ${CONTENT_FILES} ${ASSET_FILES})

# This is the important line, making sure to point to the header file
target_include_directories(${EXE_NAME} PRIVATE ${CMAKE_CURRENT_LIST_DIR}/source)
target_include_directories(${EXE_NAME} PRIVATE ${DEPENDENCIES_INCLUDE_DIRECTORIES})

set_target_properties(${EXE_NAME} PROPERTIES COMPILE_FLAGS "/Yupch.h")
set_source_files_properties(source/pch.cpp PROPERTIES COMPILE_FLAGS "/Ycpch.h")

set_property(TARGET ${EXE_NAME} PROPERTY VS_WINRT_COMPONENT TRUE)

target_link_libraries(${EXE_NAME} d3d11)
target_link_libraries(${EXE_NAME} libGLESv2 libEGL)
