import { IHeaderParams, IInnerHeaderComponent } from "ag-grid-community"

export interface ILinkHeaderParams {
  url?: string
  headerName?: string
}

export class LinkHeaderComponent implements IInnerHeaderComponent {
  private agParams!: ILinkHeaderParams & IHeaderParams
  private eGui!: HTMLDivElement
  private eText!: HTMLElement
  private eLink!: HTMLAnchorElement

  init(agParams: ILinkHeaderParams & IHeaderParams) {
    this.agParams = agParams

    const eGui = (this.eGui = document.createElement("div"))
    eGui.classList.add("link-header-component")
    eGui.style.cssText = `
            display: flex;
            align-items: center;
            justify-content: flex-start;
            height: 100%;
            width: 100%;
            box-sizing: border-box;
            overflow: visible;
            min-width: fit-content;
            padding-left: 8px;
        `

    // Do not enable auto-wrap and auto-header height, keep single line display

    // Create 🔗 link element
    if (agParams.url) {
      const eLink = (this.eLink = document.createElement("a"))
      eLink.href = agParams.url
      eLink.target = "_blank"
      eLink.rel = "noopener noreferrer"
      eLink.innerHTML = "🔗"
      eLink.style.cssText = `
                margin-right: 4px;
                font-size: 14px;
                text-decoration: none;
                color: inherit;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                flex: 0 0 auto;
            `

      // Add click event, prevent bubbling
      eLink.addEventListener("click", (e) => {
        e.stopPropagation()
      })

      eGui.appendChild(eLink)
    }

    // Create text element
    const textNode = document.createElement("span")
    this.eText = textNode
    textNode.textContent = agParams.headerName || agParams.displayName
    textNode.style.cssText = `
            flex: 1 1 auto;
            min-width: fit-content;
            overflow: visible;
            white-space: nowrap;
            text-overflow: unset;
        `
    // Hover tooltip displays full title
    const fullTitle = textNode.textContent || ""
    textNode.title = fullTitle
    eGui.title = fullTitle
    eGui.appendChild(textNode)

    // Delay setting column width to ensure DOM rendering is complete before measuring
    // Use longer delay and retry mechanism to ensure successful adjustment
    setTimeout(() => {
      this.adjustColumnWidth()
    }, 100)

    // Additional retry mechanism to ensure width adjustment succeeds
    setTimeout(() => {
      this.adjustColumnWidth()
    }, 500)
  }

  private adjustColumnWidth() {
    try {
      const col = this.agParams.column as any
      const colApi = (this.agParams as any).columnApi
      const gridApi = (this.agParams as any).api

      if (!col || !colApi || !gridApi) {
        console.warn(
          "LinkHeaderComponent: Missing required APIs for width adjustment"
        )
        return
      }

      // Get current column's actual width
      const currentWidth =
        col.getActualWidth?.() || col.getColDef?.()?.width || 100

      // Measure actual width needed for text
      const text = this.eText.textContent || ""
      const textWidth = this.measureTextWidth(text)

      // Calculate total required width
      const paddingLeft = 8
      const iconWidth = this.agParams.url ? 20 : 0
      const iconGap = this.agParams.url ? 4 : 0
      const extra = 30 // Right padding + sorting/filter icon space
      const requiredWidth = Math.max(
        textWidth + paddingLeft + iconWidth + iconGap + extra,
        150 // Set minimum width to 150px to ensure text is not over-compressed
      )

      console.log(
        `LinkHeaderComponent [${text}]: currentWidth=${currentWidth}, requiredWidth=${requiredWidth}, textWidth=${textWidth}`
      )

      // If current width is insufficient, expand column width
      if (requiredWidth > currentWidth) {
        const newWidth = Math.ceil(requiredWidth)

        // Use gridApi's setColumnWidths method, more reliable
        try {
          const colId = col.getColId?.() || col.getColDef?.()?.field
          if (colId) {
            gridApi.setColumnWidths([{ key: colId, newWidth }])
            console.log(
              `LinkHeaderComponent [${text}]: Successfully set width to ${newWidth}px using gridApi.setColumnWidths`
            )
            return // Exit if successful
          }
        } catch (e) {
          console.warn(
            `LinkHeaderComponent [${text}]: gridApi.setColumnWidths failed:`,
            e
          )

          // If setColumnWidths fails, try columnApi
          try {
            colApi.setColumnWidth(col, newWidth)
            console.log(
              `LinkHeaderComponent [${text}]: Successfully set width to ${newWidth}px using columnApi.setColumnWidth`
            )
            return // Exit if successful
          } catch (e2) {
            console.warn(
              `LinkHeaderComponent [${text}]: columnApi.setColumnWidth failed:`,
              e2
            )

            // Final fallback: directly set colDef
            const colDef = col.getColDef?.()
            if (colDef) {
              colDef.width = newWidth
              // Also set minWidth to ensure width won't be compressed
              colDef.minWidth = Math.min(newWidth, 150)
              gridApi.refreshHeader()
              console.log(
                `LinkHeaderComponent [${text}]: Set width ${newWidth}px via colDef as fallback`
              )
            }
          }
        }
      } else {
        console.log(
          `LinkHeaderComponent [${text}]: Current width ${currentWidth}px is sufficient`
        )
      }
    } catch (error) {
      console.warn("LinkHeaderComponent: Failed to adjust column width:", error)
    }
  }

  private measureTextWidth(text: string): number {
    try {
      // Create temporary element to measure text width
      const temp = document.createElement("span")
      temp.style.cssText = `
        position: absolute;
        visibility: hidden;
        white-space: nowrap;
        font-family: inherit;
        font-size: inherit;
        font-weight: inherit;
      `
      temp.textContent = text
      document.body.appendChild(temp)

      const width = temp.offsetWidth
      document.body.removeChild(temp)

      return width
    } catch (_) {
      // Fallback to canvas measurement
      try {
        const canvas = document.createElement("canvas")
        const ctx = canvas.getContext("2d")
        if (ctx) {
          ctx.font = window.getComputedStyle(this.eText).font
          return Math.ceil(ctx.measureText(text).width)
        }
      } catch (_) {
        // Final fallback: estimate width
        return text.length * 8
      }
    }
    return 0
  }

  getGui() {
    return this.eGui
  }

  refresh(params: ILinkHeaderParams & IHeaderParams) {
    // Update parameters
    this.agParams = params

    // Update link
    if (params.url && this.eLink) {
      this.eLink.href = params.url
    }

    // Update text content
    const newText = params.headerName || params.displayName
    const oldText = this.eText.textContent

    if (newText !== oldText) {
      this.eText.textContent = newText
      const fullTitle = newText || ""
      this.eText.title = fullTitle
      this.eGui.title = fullTitle

      // Re-adjust column width (multiple attempts to ensure success)
      setTimeout(() => {
        this.adjustColumnWidth()
      }, 100)

      setTimeout(() => {
        this.adjustColumnWidth()
      }, 500)
    }

    return true
  }
}

export default LinkHeaderComponent
