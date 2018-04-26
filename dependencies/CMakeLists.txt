#########
# Angle
message(STATUS "Adding angle")
add_subdirectory(angle ${CMAKE_CURRENT_BINARY_DIR}/dependencies/angle)

set(ANGLE_FOLDER "Dependencies/Angle")

set(ANGLE_TARGETS
    libEGL
    libANGLE
    libGLESv2
    angle_common
    angle_image_util
    angle_preprocessor
    angle_translator    
)

foreach(ANGLE_TARGET ${ANGLE_TARGETS})
    set_target_properties (${ANGLE_TARGET} PROPERTIES FOLDER ${ANGLE_FOLDER})
endforeach()

set(DEPENDENCIES_INCLUDE_DIRECTORIES 
    ${DEPENDENCIES_INCLUDE_DIRECTORIES} 
    "${CMAKE_CURRENT_LIST_DIR}/angle/include" 
    PARENT_SCOPE
)
